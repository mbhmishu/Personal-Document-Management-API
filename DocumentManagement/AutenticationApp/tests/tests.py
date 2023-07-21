from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounts.models import User,Profile
from ..serializers import ProfileSerializer




class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('account:register')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
        }
        self.invalid_payload = {
            'email': 'invalidemail',
            'password': 'password123',
            'password2': 'password123',
        }
    
    def test_valid_registration(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_invalid_registration(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('account:login')
        self.user = get_user_model().objects._create_user(
            email='test@example.com',
            password='password123'
        )
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }
    
    def test_valid_login(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data["token"])
        self.assertIn('refresh', response.data['token'])
    

    def test_invalid_login(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserPasswordChangeTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('account:password_change')
        self.user = get_user_model().objects._create_user(
            email='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'password': 'password123',
            'password': 'newpassword123',
            'password2': 'newpassword123',
        }
        self.invalid_payload = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123',
        }
    
    def test_valid_password_change(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
        {'msg': 'Password change succesfully!'})
    
    def test_invalid_password_change(self):
         response = self.client.post(self.url, data=self.invalid_payload)
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetByEmailTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('account:password-reset-link')
        self.user = get_user_model().objects._create_user(
            email='test@example.com',
            password='password123'
        )
        self.valid_payload = {
            'email': 'test@example.com',
        }
        self.invalid_payload = {
            'email': 'invalidemail',
        }
    
    def test_valid_password_reset_email(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)
    
    def test_invalid_password_reset_email(self):
        response = self





class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects._create_user(
            email='test@example.com',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):

        url = reverse('account:profile-update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        





    def test_update_profile(self):
        url = reverse('account:profile-update')
        data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'address_1': '123 Main St',
            'city': 'Anytown',
            'zipcode': '12345',
            'country': 'USA',
            'phone': '555-1234'
        }
        response = self.client.put(url, data,)
        
        response = self.client.put(url, data)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print(response.data['detail'])  # prints the validation errors


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['full_name'], data['full_name'])


    