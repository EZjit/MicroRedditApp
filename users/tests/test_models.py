import pytest
from django.db import IntegrityError
from mixer.backend.django import mixer
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def valid_user():
    return mixer.blend(User, email='test@example.com', username='johnsmith')


# Test objects creation

def test_create_user(valid_user):
    user = valid_user
    assert user.email == 'test@example.com'
    assert user.username == 'johnsmith'
    assert user.avatar.name == 'avatar.svg'
    assert user.created_at is not None
    assert user.is_staff is False
    assert user.is_superuser is False


def test_create_superuser():
    superuser = User.objects.create_superuser(
        username='superuser',
        email='test@example.com',
        password='9Ij8uH7yG',
        )
    assert superuser.email == 'test@example.com'
    assert superuser.username == 'superuser'
    assert superuser.avatar.name == 'avatar.svg'
    assert superuser.created_at is not None
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


# Test model methods

def test_user_str(valid_user):
    assert str(valid_user) == 'test@example.com'


# Test uniqueness constraints

def test_user_email_unique(valid_user):
    user1 = valid_user
    with pytest.raises(IntegrityError) as e:
        mixer.blend(User, email=user1.email)
    assert 'UNIQUE constraint failed' in str(e.value)
    assert 'user.email' in str(e.value)


def test_user_username_unique(valid_user):
    user1 = valid_user
    with pytest.raises(IntegrityError) as e:
        mixer.blend(User, username=user1.username)
    assert 'UNIQUE constraint failed' in str(e.value)
    assert 'user.username' in str(e.value)
