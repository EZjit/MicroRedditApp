from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email adress',
        unique=True,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
