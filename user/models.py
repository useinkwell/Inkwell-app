from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
    )

	
class AccountManager(BaseUserManager):

    def create_user(self, email, user_name, first_name, 
                                            password, **other_fields):
        if not email:
            return ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self, email, user_name, first_name, 
                                            password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        

        return self.create_user(email, user_name, first_name, 
                                            password, **other_fields)


# create the custom user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)    
    date_registered = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']
    objects = AccountManager()

    def __str__(self) -> str:
        return self.user_name
