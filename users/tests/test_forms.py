import pytest
from users.forms import CustomUserChangeForm, CustomUserCreationForm

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'username, email, password1, password2, validity', [
        ('johnsmith', 'test@example.com', '9iJ8Uh7yG', '9iJ8Uh7yG', True),  # Correct data
        ('a' * 200, 'test@example.com', '9iJ8Uh7yG', '9iJ8Uh7yG', False),  # Username should be 150 characters maximum
        ('johnsmith', 'dasdasdas', '9iJ8Uh7yG', '9iJ8Uh7yG', False),  # Email should be valid
        ('johnsmith', '', '9iJ8Uh7yG', '9iJ8Uh7yG', False),  # Email can't be blank
        ('johnsmith', 'test@example.com', '9iJ8Uh7yG', '9iJ8Uh7y', False),  # Password1 should be equal to password2
        ('johnsmith', 'test@example.com', '9ij8uh7yg', '9ij8uh7yg', False),  # Password should contain at least one uppercase letter
    ])
def test_user_creation_form(username, email, password1, password2, validity):
    form = CustomUserCreationForm(data={
        'username': username,
        'email': email,
        'password1': password1,
        'password2': password2,
    })
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    'username, validity', [
        ('johnsmith', True),  # Correct data
        ('a' * 200, False),  # Username should be 150 characters maximum
    ])
def test_user_change_form(username, validity):
    form = CustomUserChangeForm(data={
        'username': username,
    })
    assert form.is_valid() is validity
