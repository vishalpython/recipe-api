from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate # authenticate is django helper  commend simply pass username and password
from recipe_api import models
from django.utils.translation import ugettext_lazy as _


class UserModelSerializers(serializers.ModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        """created new user with encrepeted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update the user and seeting password correctley and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSeralizer(serializers.Serializer):
    """Seralizer for user  object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authanticate the user here attrs is dict type which conatil all paramaeter"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = ("unable to authenticate with provide credentails")
            raise serializers.ValidationError(msg, code="authencation")

        attrs['user'] = user

        return attrs