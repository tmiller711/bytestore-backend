from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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