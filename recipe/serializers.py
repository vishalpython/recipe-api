from rest_framework import serializers
from recipe_api import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id','name')
        read_only_fields = ('id',)

class IngridentSerializer(serializers.ModelSerializer):

    class meta:
        model = models.Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)
