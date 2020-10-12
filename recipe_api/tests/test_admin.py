from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import admin


class AdminSiteTestes(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
           email="vishal889@gmaill.com",
           password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
           email = "vish889@gmail.com",
           password = 'password123',
           name = 'vishal'
        )

    def test_useer_listed(self):
        """Test that user are listed on user page"""
        url = reverse('admin:recipe_api_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response,self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page work"""
        url = reverse('admin:recipe_api_user_change', args = [self.user.id])
        #/admin/recipe_api/user/<user_id>
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page work"""
        url = reverse('admin:recipe_api_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)        
