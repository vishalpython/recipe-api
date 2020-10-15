from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from recipe_api.models import Ingredient
from recipe.serializers import IngridentSerializer
from django.test import TestCase
from django.contrib.auth import get_user_model


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngridentApiTest(TestCase):
    """Test the publicly available ingrident api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to asses the endpoint"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetIngrredientsApiTest(TestCase):
    """test the privet ingrident api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            'vishalgore889@gmail.com',
            'pass123'
        )

        self.client.force_authenticate(self.user)

    def test_retrive_ingrident_list(self):
        """Test retrieving a list of ingrident"""
        Ingredient.objects.create(user = self.user, name= "masala")
        Ingredient.objects.create(user = self.user, name= 'salt')

        res = self.client.get(INGREDIENTS_URL)

        serializer = IngridentSerializer(Ingredient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingrident_limited_to_user(self):
        """Test that ingrident is for authanticated user and return it"""
        user2 = get_user_model().objects.create_user(
            'vish889@gmail.com',
            'passw123'
        )

        Ingredient.objects.create(user = user2, name='chicken-masaala')
        ingrident = Ingredient.objects.creeate(user = self.user, name="turmic")

        res = self.client.get(Ingredient)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingrident.name)


