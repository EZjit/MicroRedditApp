from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
