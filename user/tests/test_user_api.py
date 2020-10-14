from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
USER_TOKEN_URL = reverse('user:token')

def create_user(**params): #**params is dynmic list of arguments
    """This is the helper fuction to create user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user API(public)"""
    def setUp(self):
        self.client =APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            'email': 'vishalgore889@gmail.com',
            'password' : 'vishal',
            'name' : 'vishal'
        }
        res = self.client.post(CREATE_USER_URL, payload)  #make request to create useer
        self.assertEqual(res.status_code, status.HTTP_201_CREATED) #test outcome what we execpect
        user = get_user_model().objects.get(**res.data) #test  that object is actully  created
        self.assertTrue(user.check_password(payload['password']))#test that our password is correct
        self.assertNotIn('password',res.data)#check that password is not return to user

    def test_user_exist(self):
        """Test creating a user that already exist fails"""
        payload = {
            'email': 'vishalgore889@gmail.com',
            'password' : 'vishal',
            'name' : 'vishal'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
         """Test that password must be more than 5 characters"""
         payload = {
             'email': 'vishalgore889@gmail.com',
             'password' : 'vishal',
             'name' : 'vishal'
         }
         res = self.client.post(CREATE_USER_URL, payload)
         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

         user_exist = get_user_model().objects.filter(
             email = payload['email']
         ).exists()

         self.assertFalse(user_exist)#we dnt want to be user exists  will false

    def test_create_user_for_token(self):
        """Test that token is created for the user"""
        payload = {'email':'vishalggore889@gmail.com','passworrd':'vishal'}
        create_user(**payload)
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertIn('token', res.data) #check token in res.data
        self.assertEqual(res.status_code, status.HTTP_200_OK)#it check equle for status code

    def test_create_token_invalid(self):
        """Test thst token is not created if invalid credetails aree given"""
        create_user(email = 'vishalgore889@gmail.com',password = 'vishal123')
        payload = {
            'email':'vishalgore889@gmail.com',
            'password' : 'vishal'
        }
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user is not exist"""
        payload = {'email':'vishalgore889@gmail.com', 'password':'vishal123'}
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        res = self.client.post(USER_TOKEN_URL, {'email':'vishalgore889@gmail.com','password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)