from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe_api import models


def sample_user(email='vishalgore889@gmail.com',password='vishal123'):
    return get_user_model().objects.create_user(email,password)


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

    def test_create_new_superuser(self):
        """Test Creating a new superuser"""
        user = get_user_model().objects.create_superuser(
        'vishalgore889@gmail.com',
        '1456'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string repestions"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Non-Veg'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredint_str(self):
        """Test the ingredint string respretion"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name = "cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_object_create(self):
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title="chicken",
            time_minuts=5,
            price=250.00
        )

        self.assertEqual(str(recipe), recipe.title)
    @patch('uuid.uuid4')
    def test_recpe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path,exp_path)