from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe_api.models import Tag,Ingredient

from recipe import serializers


class TagViewset(viewsets.GenericViewSet,
                 mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the dataase"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return object for current auntheactited user  only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag and aasigne to the current user"""
        print("doneeeeee")
        serializer.save(user=self.request.user)


class IngredientViewset(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage ingriedent in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngridentSerializer

    def get_queryset(self):
        """Return object for the current authhenticated user"""
        return self.queryset.filter(user = self.request.user).order_by('-name')

    def perform_create(self, serializer): # method of ceerateemodelmixin
        """Create a new ingredient"""
        serializer.save(user = self.request.user)


