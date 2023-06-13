from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class RegisterApiViewTest(APITestCase):
    def test_register_user(self):
        url = reverse('register')

        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])

    def test_register_user_invalid_email(self):
        url = reverse('register')
        data = {
            'email': 'susanthl199gmail.com',
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_username(self):
        url = reverse('register')
        data = {
            'email': 'susanthl199gmail.com',
            'username': '',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_password(self):
        url = reverse('register')
        data = {
            'email': 'susanthl1998+50@gmail.com',
            'username': 'susanth56',
            'password': 'tes'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)