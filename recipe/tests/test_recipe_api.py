from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe_api.models import Recipe
from recipe.serializers import Recipeserializer


RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return sample recipe"""
    defaults ={
        'title': 'sample_recipe',
        'time_minuts': 10,
        'price': 500.00
    }
    #what if we want to custmize this values
    #for  perticular  recipe for preticular test
    #any parameters you pass in after thee user in sample_recipe() fn
    #will overide the default
    #we do thatv using update function

    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PubliceRecipeApiTest(TestCase):
    """Test that authentication is required"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test that authentication is required"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetRecipeApi(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'vishalgore889@gmail.com',
            'password123'
        )
        self.client.force_authenticate(self.user)

    def retrive_recipe(self):
        """Test retriveng a list of recipe"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serailzer =  Recipeserializer(recipe,many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serailzer.data)

    def test_recipe_limited_to_user(self):
        """Test retriving recipe for the user"""
        user2 = get_user_model().objects.create_user(
            'vish@gmail.com',
            'passwordqwe'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.filter(user = self.user)
        serializer =  Recipeserializer(recipe,many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data, serializer.data)