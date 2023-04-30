from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'avatar']
