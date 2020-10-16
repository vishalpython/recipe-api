import tempfile #generate a temporary files so what is dose is allow you to  call a fun
#which will create a temp file somewhere in the sysytm that you can remove that file after
#you have used  it
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe_api.models import Recipe, Ingredient, Tag
from recipe.serializers import Recipeserializer,  RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    """Return url for reciipe image upload"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])

def detail_url(recipe_id):
    """Return recipe  details url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user,name='main-coures'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user,name = 'cinnoan'):
    """create and return a sample ingredient"""
    return Ingredient.objects.create(user=user,name=name)



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

    def test_view_recipe_details(self):
         """Test viewing a recipe details"""
         recipe = sample_recipe(user=self.user)
         recipe.tags.add(sample_tag(user=self.user))
         recipe.ingredient.add(sample_ingredient(user=self.user))

         url = detail_url(recipe.id)
         res = self.client.get(url)

         serailzer = RecipeDetailSerializer(recipe)
         self.assertEqual(res.data, serailzer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {
            'title': 'Chocklet cheescake',
            'time_minuts': 30,
            'price' : 500
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # when you create an objects using django restframework
        #deafult behavior is that it will  return a dictonary containg created object
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe,key)) # getattr(recipe,key) == recipe.title ..
            #getattr is a function that come with python that allow you to
            #retrieve an attribute  from an objects by passing in a veriable

    def test_create_recipe_with_tag(self):
        """Test creating recipe with tag"""
        tag1 = sample_tag(user=self.user, name = 'Vegen')
        tag2 = sample_tag(user=self.user, name='Dessert')

        payload = {
            'title': 'Avocado lime cheescake',
            'tags' : [tag1.id, tag2.id],
            'time_minuts': 50,
            'price': 400
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(),2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2,tags)

    def test_create_recipe_with_ingredient(self):
        """test creating recipe with ingrident"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingrident2 = sample_ingredient(user=self.user, name ='Ginger')

        payload = {
            'title': 'Thai prawn and curry',
            'ingredient': [ingredient1.id,ingrident2.id],
            'time_minuts':60,
            'price': 250
        }
        res = self.client.post(RECIPE_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredient.all()
        self.assertEqual(ingredients.count(),2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingrident2,ingredients)

    def test_partial_update_recipe(self):
        """Test updating recipe with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name= 'curry')

        payload = {
            'title':'chicken tikka', 'tags':[new_tag.id]

        }
        url = detail_url(recipe.id)

        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])

        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_reecipe(self):
        """Test updating recipe with put"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user = self.user))
        payload = {
            'title': 'mutton curry',
            'time_minuts': 45,
            'price':450

        }
        url = detail_url(recipe.id)
        self.client.put(url , payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minuts, payload['time_minuts'])
        self.assertEqual(recipe.price, payload['price'])
        tags =recipe.tags.all()
        self.assertEqual(len(tags), 0 )


class RecipeImageLoadTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'vishalgore8899@gmail.com',
            'vishal123'
        )
        self.client.force_authenticate(self.user)
        self.recipe= sample_recipe(user = self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_uploading_image_to_recipe(self):
        """Test uploading image to the recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB',(10,10))
            img.save(ntf,format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image':  ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image':'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)










