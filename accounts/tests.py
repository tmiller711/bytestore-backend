from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import AccessToken

from .tokens import accounts_activation_token
from .models import Account
# Create your tests here.

class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_valid_data(self):
        data = {"email": 'test@gmail.com', 'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().email, 'test@gmail.com')
        self.assertEqual(Account.objects.get().username, 'testuser')
        self.assertFalse(Account.objects.get().is_active)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your Account')
        self.assertEqual(mail.outbox[0].to, ['test@gmail.com'])

    def test_register_invalid_data(self):
        data = {'email': 'invalid_email', 'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 0)

        # test missing username
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 0)

        # test missing password
        data = {'email': 'test@example.com', 'username': 'testuser'}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 0)

class ActivateTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testuser',
            password='testpassword'
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = accounts_activation_token.make_token(self.user)

    def test_user_activation_success(self):
        url = reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_user_activation_failure_bad_uidb64(self):
        url = reverse('activate', kwargs={'uidb64': 'invaliduidb64', 'token': self.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_user_activation_failure_bad_token(self):
        url = reverse('activate', kwargs={'uidb64': self.uid, 'token': 'invalidtoken'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

class LogoutTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass'
        )
        self.user.is_active = True
        self.user.save()
        self.token = AccessToken.for_user(self.user)

    # def test_logout_success(self):
    #     # Set up the HTTP Authorization header with the token
    #     headers = {'Authorization': f'Bearer {str(self.token)}'}

    #     # Send a GET request to the logout URL
    #     url = reverse('logout')
    #     response = self.client.get(url, **headers)

    #     # Assert that the response status code is 200 OK
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Assert that the token has been blacklisted
    #     blacklisted_token = AccessToken(self.token['access'])
    #     self.assertTrue(blacklisted_token.blacklisted)
    
    def test_logout_failure(self):
        # Send a GET request to the logout URL without an Authorization header
        url = reverse('logout')
        response = self.client.get(url, format='json')

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@gmail.com'
        )
        self.user.is_active = True
        self.user.save()
        self.url = reverse('token_obtain_pair')

    def test_token_obtain_pair_view_valid(self):
        # Test valid login
        response = self.client.post(self.url, {'email': 'testuser@gmail.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_token_obtain_pair_view_invalid(self):
        # Test invalid login
        response = self.client.post(self.url, {'email': 'testuser@gmail.com', 'password': 'wrongpass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('access' in response.data)
        self.assertFalse('refresh' in response.data)
        self.assertFalse('email' in response.data)
        self.assertFalse('username' in response.data)