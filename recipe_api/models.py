from django.db import models
from django.contrib.auth.models import (
                           AbstractBaseUser,
                           BaseUserManager,
                           PermissionsMixin
)
from django.conf import settings

class UserModelManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save a superuser"""
        user = self.create_user(email, password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user 



class User(AbstractBaseUser,PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=225,unique=True)
    name =  models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserModelManager()

    USERNAME_FIELD='email'


class Tag(models.Model):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=225)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name
