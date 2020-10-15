from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe_api.models import Tag
from django.urls import reverse
from recipe.serializers import TagSerializer
TAGS_URL = reverse('recipe:tag-list')


class PublicTagApiTest(TestCase):
    """Test the pulicly availabe api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is require for retrive thee tag"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApi(TestCase):
    """test the authorized  use tags api"""

    def setUp(self):
        """Test retriving tag"""
        self.user = get_user_model().objects.create_user(
            'vishalgore889@gmail.com',
            'password123'
        )
        self.client =APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        """Test retriving tags"""
        Tag.objects.create(user=self.user,name='non-veg')
        Tag.objects.create(user=self.user,name='Dessert')

        res = self.client.get(TAGS_URL)
        tag = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tag, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tag_limited_to_user(self):
        """Test that tag return for the autenticated  user"""
        user2 = get_user_model().objects.create_user(
            'vishal@gmail.com',
            'pass123'
        )
        Tag.objects.create(user=user2,name='Fruity')
        tag = Tag.objects.create(user=self.user,name='comfort food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)

    def test_create_tag_successful(self):
         """Test creating a new tags"""
         payload = {
             'name':'test tag'
         }

         self.client.post(TAGS_URL, payload)
         exist =Tag.objects.filter(
             user=self.user,
             name = payload['name']
         ).exists()
         self.assertTrue(exist)

    def test_create_tag_invalid(self):
        """Test creating a tang with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

