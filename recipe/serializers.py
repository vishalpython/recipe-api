from rest_framework import serializers
from recipe_api import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id','name')
        read_only_fields = ('id',)

class IngridentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)

class Recipeserializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many =True,
        queryset = models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = (
                  'id', 'title', 'ingredient', 'tags',
                  'time_minuts', 'price', 'link'
                  )
        read_only_fields = ('id',)


class  RecipeDetailSerializer(Recipeserializer):

    """Seralizer rhe recipe detils by reuseing code"""
    ingredient = IngridentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)



