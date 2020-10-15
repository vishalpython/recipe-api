from rest_framework import serializers
from recipe_api import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'
        read_only_fields = ('id',)