from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe_api.models import Tag,Ingredient,Recipe

from recipe import serializers


class BaseClassView(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticate system"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new object"""
        serializer.save(user=self.request.user)


class TagViewset(BaseClassView):
    """Manage tags in the dataase"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewset(BaseClassView):
    """Manage ingriedent in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngridentSerializer


class RecipeApiView(viewsets.ModelViewSet):
    """Manage recipe in the database"""
    serializer_class = serializers.Recipeserializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrive the recipe for the authentictaed user"""
        return self.queryset.filter(user = self.request.user)
