from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core import mail

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