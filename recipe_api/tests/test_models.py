from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'vishalgore889@gmail.com'
        password = "vishal123"
        user = get_user_model().objects.create_user(
        email=email,
        password=password
        )


        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user normalized"""
        email = "vishal@GMAIL.COM"
        user = get_user_model().objects.create_user(
        email, "15448"
        )

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '1515')
