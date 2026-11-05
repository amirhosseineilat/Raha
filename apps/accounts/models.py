from django.db import models
from django.contrib.auth.models import AbstractUser ,UserManager

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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email