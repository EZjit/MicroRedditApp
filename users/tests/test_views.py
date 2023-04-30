import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from pytest_django.asserts import assertTemplateUsed
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User

pytestmark = pytest.mark.django_db


# Test signup view

def test_initial_signup_view(client):
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'registration/signup.html')
    assert isinstance(response.context['form'], CustomUserCreationForm)


def test_successful_signup(client):
    url = reverse('signup')
    user_data = {
        'username': 'johnsmith',
        'email': 'test@example.com',
        'password1': '9iJ8Uh7yG',
        'password2': '9iJ8Uh7yG',
    }

    response = client.post(url, user_data)
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert User.objects.first().username == 'johnsmith'


# Test show_profile view

@pytest.fixture
def create_page_content():
    user = mixer.blend(User)
    communities = mixer.cycle(7).blend('core.Community')
    posts = mixer.cycle(10).blend('core.Post', user=user)
    comments = mixer.cycle(20).blend('core.Comment')
    return {'user': user, 'communities': communities, 'posts': posts, 'comments': comments}


def test_show_profile_view(client, create_page_content):
    user = create_page_content['user']
    response = client.get(reverse('profile', args=[user.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'users/profile.html')


def test_show_profile_context(client, create_page_content):
    user = create_page_content['user']
    response = client.get(reverse('profile', args=[user.id]))
    assert response.context['user'] == user
    assert response.context['communities'].count() == 5
    assert response.context['user_posts'].count() == 10
    assert response.context['recent_comments'].count() == 10


def test_show_profile_view_with_invalid_user_id(client):
    response = client.get(reverse('profile', args=[999]))
    assert response.status_code == 404


# Test edit_profile view

@pytest.fixture
def create_user_and_login(client):
    user = mixer.blend(User)
    client.force_login(user)
    return user


def test_edit_profile_view_get_request(client, create_user_and_login):
    url = reverse('edit-profile')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'users/edit_profile.html')
    assert isinstance(response.context['form'], CustomUserChangeForm)


def test_edit_profile_view_post_requrest(client, create_user_and_login):
    user = create_user_and_login
    url = reverse('edit-profile')

    data = {'username': 'brand_new_username'}

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('profile', args=[user.id])
    user.refresh_from_db()
    assert user.username == 'brand_new_username'


def test_edit_profile_view_not_logged_in(client):
    mixer.blend(User)
    url = reverse('edit-profile')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('edit-profile')


# Test delete_profile view

def test_delete_profile_view_get_request(client, create_user_and_login):
    user = create_user_and_login
    url = reverse('delete-profile')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed('delete.html')
    assert response.context['object'] == user


def test_delete_profile_view_post_request(client, create_user_and_login):
    user = create_user_and_login
    response = client.post(reverse('delete-profile'))
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert not User.objects.filter(id=user.id).exists()


def test_delete_profile_view_not_logged_in(client):
    mixer.blend(User)
    url = reverse('delete-profile')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('delete-profile')
