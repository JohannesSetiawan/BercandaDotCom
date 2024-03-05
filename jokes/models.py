from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    api_keys = models.CharField(max_length=70)

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

class Jokes(models.Model):
    joke = models.TextField()
    creator = models.ForeignKey(AppUser, unique=False, on_delete=models.CASCADE, related_name='jokes')
    categories = models.ManyToManyField(Category)