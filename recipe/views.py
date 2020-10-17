from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe_api.models import Tag,Ingredient,Recipe

from recipe import serializers


class BaseClassView(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticate system"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by('-name').distinct()

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
    queryset = Recipe.objects.all()
    serializer_class = serializers.Recipeserializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_int(self, qs):
        """Convert the list of string IDs to list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrive the recipe for the authentictaed user"""
        tags = self.request.query_params.get('tags')
        ingredient = self.request.query_params.get('ingredient')
        queryset = self.queryset
        if tags:
            tags_id = self._params_to_int(tags)
            queryset = queryset.filter(tags__id__in =tags_id)
        if ingredient:
            ingredient_id = self._params_to_int(ingredient)
            queryset = queryset.filter(ingredient__id__in = ingredient_id)

        return queryset.filter(user = self.request.user)

    def get_serializer_class(self):
        #overide function this is a fun that called to retrive the serailizer class
        #for perticular request
        #this fun are used for wanted to chang the serailzer class for the different action
        #that are available on the recip0e  viewset

        """Return approprite seralizer class"""
        if self.action == 'retrieve':
            print('okkkkkkkkkkkkw')
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            print('okkkkkkkkkkkkkkkkk')
            return serializers.RecipeImageSerailzer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True,url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to the recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )