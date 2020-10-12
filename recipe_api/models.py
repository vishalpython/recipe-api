from django.db import models
from django.contrib.auth.models import (
                           AbstractBaseUser,
                           BaseUserManager,
                           PermissionsMixin
)


class UserModelManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=225,unique=True)
    name =  models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserModelManager()

    USERNAME_FIELD='email'
