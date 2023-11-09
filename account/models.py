from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):

  def create_user(self, email, username, password=None, **extra_fields):
    """Create, save and return a new user."""

    if not email:
      raise ValueError('User must have an email address.')

    user = self.model(email=self.normalize_email(email),username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  # def create_staffuser(self, email, password):
  #   """Create and return a new staffuser"""
  #   user = self.create_user(email, password)
  #   user.is_staff = True
  #   user.is_superuser = False
  #   user.save(using=self._db)

  #   return user

  def create_superuser(self, email,username, password):
    """Create and return a new superuser"""

    user = self.create_user(email,username, password)
    user.is_staff = True
    user.is_superuser =True
    user.save(using=self._db)

    return user


class User(AbstractBaseUser, PermissionsMixin):

  email = models.EmailField(max_length=255, unique=True)
  username = models.CharField(max_length=255)
  phone = models.CharField(max_length=20, blank=True, null=True)
  occupation = models.CharField(max_length=255, blank=True, null=True)
  company = models.CharField(max_length=255, blank=True, null=True)
  bio = models.TextField(max_length=455, blank=True, null=True)
  profile_picture = models.ImageField(upload_to='profile_pictures',default= 'profile_pictures/user-default.jpg', blank=True, null=True)
  joined = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.username

