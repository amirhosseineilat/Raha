from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    username = models.CharField(
    max_length=150,
    unique=True,
    null=True,
    blank=True,
    )

    email = models.EmailField(
        unique=True,
        max_length=254,
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email