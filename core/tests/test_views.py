import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from pytest_django.asserts import assertTemplateUsed
from core.forms import CommentForm
from core.models import Community, Post, Comment

pytestmark = pytest.mark.django_db


# Fixture for login_required views
@pytest.fixture
def create_user_and_login(client):
    user = mixer.blend('users.User')
    client.force_login(user)
    return user


# Fixture populates db for testing home page and communities views
@pytest.fixture
def create_context():
    communities = mixer.cycle(5).blend(Community)
    python_community = mixer.blend(Community, name='Python')
    posts = mixer.cycle(30).blend(Post, community=(community for community in communities*6))
    python_posts = mixer.cycle(13).blend(Post, community=python_community)
    mixer.cycle(90).blend(Comment, post=(post for post in posts*3))
    mixer.cycle(26).blend(Comment, post=(post for post in python_posts*2), parent=None)
    return {
        'communities': Community.objects.all(),
        'python_community': python_community,
        'posts': Post.objects.all(),
        'python_posts': Post.objects.filter(community__name__icontains='Python'),
        'comments': Comment.objects.all(),
        'python_comments': Comment.objects.filter(post__community__name__icontains='Python'),
    }


# Fixture for show post testing
@pytest.fixture
def create_post_page_context():
    post = mixer.blend(Post)
    mixer.cycle(5).blend(Comment, post=post)
    return post


# Fixture for edit post testing
@pytest.fixture
def create_post_page_edit_context(client):
    user = mixer.blend('users.User')
    client.force_login(user)
    post = mixer.blend(Post, user=user)
    return {'user': user, 'post': post}


# ------------------Testing home page view-------------------

# Tests without a query string

def test_initial_home_page_status_code_and_template(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')


def test_initial_home_page_context(client):
    response = client.get(reverse('home'))
    assert 'page_obj' in response.context
    assert 'number_of_posts' in response.context
    assert 'communities' in response.context
    assert 'community_comments' in response.context
    assert response.context['query'] == ''


# Tests with a query string

def test_home_page_returning_context_with_query_string(client, create_context):
    python_community = create_context['python_community']
    url = reverse('home')

    response = client.get(url, {'q': str(python_community)})

    assert response.context['query'] == str(python_community)
    assert response.context['number_of_posts'] == create_context['posts'].count()
    assert list(response.context['communities']) == list(create_context['communities'][:5])
    assert list(response.context['page_obj']) == list(create_context['python_posts'])[:10]
    assert list(response.context['community_comments']) == list(create_context['python_comments'])[:10]


def test_home_page_pagination_without_query_string(client, create_context):
    response = client.get(reverse('home'))
    assert list(response.context['page_obj']) == list(create_context['posts'][:10])

    response = client.get(reverse('home'), {'page': 2})
    assert list(response.context['page_obj']) == list(create_context['posts'][10:20])

    response = client.get(reverse('home'), {'page': 5})
    assert list(response.context['page_obj']) == list(create_context['posts'][40:])


def test_home_page_pagination_with_query_string(client, create_context):
    python_community = create_context['python_community']
    url = reverse('home')

    response = client.get(url, {'q': str(python_community)})
    assert list(response.context['page_obj']) == list(create_context['python_posts'])[:10]

    response = client.get(url, {
        'q': str(python_community),
        'page': 2,
        })
    assert list(response.context['page_obj']) == list(create_context['python_posts'])[10:]


# ------------------Testing community views-------------------

# Test CommunityCreate class view

def test_community_create_view_get_request(client, create_user_and_login):
    response = client.get(reverse('create-community'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'core/community_form.html')


def test_community_creation_post_request(client, create_user_and_login):
    url = reverse('create-community')
    data = {
        'name': 'Community name',
        'description': 'Some description, bla bla bla'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert Community.objects.first().name == 'Community name'


def test_community_create_view_not_logged_in(client):
    response = client.get(reverse('create-community'))
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('create-community')


# Test communities page view

def test_communities_page_view_without_query_string(client, create_context):
    response = client.get(reverse('communities'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'core/communities_page.html')
    assert list(response.context['communities']) == list(create_context['communities'])


def test_communities_page_view_with_query_string(client, create_context):
    python_community = create_context['python_community']
    response = client.get(reverse('communities'), {'q': 'Python'})
    assert response.status_code == 200
    assert response.context['communities'].first() == python_community
    assert response.context['communities'].last() == python_community


# -----------------------Test post views-----------------------

# Test PostCreate class view

def test_post_create_view_get_request(client, create_user_and_login):
    response = client.get(reverse('create-post'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'core/post_form.html')


def test_post_create_view_post_request(client, create_user_and_login):
    community = mixer.blend(Community)
    url = reverse('create-post')
    data = {
        'community': community.id,
        'title': 'title',
        'body': 'body',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert Post.objects.first().title == 'title'


def test_post_create_view_not_logged_in(client):
    response = client.get(reverse('create-post'))
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('create-post')


# Test show_post view

def test_show_post_view_status_code_and_template(client, create_post_page_context):
    post = create_post_page_context
    response = client.get(reverse('post', args=[post.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'core/post_detail.html')


def test_show_post_view_context(client, create_post_page_context):
    post = create_post_page_context
    response = client.get(reverse('post', args=[post.id]))
    assert response.context['post'] == post
    assert response.context['post_comments_num'] == post.comments.count()
    assert isinstance(response.context['comment_form'], CommentForm)
    assert list(response.context['post_top_level_comments']) == list(post.get_comments())


def test_show_post_view_with_invalid_post_id(client):
    response = client.get(reverse('profile', args=[999]))
    assert response.status_code == 404


def test_show_post_view_add_comment(client,
                                    create_post_page_context,
                                    create_user_and_login):
    post = create_post_page_context
    url = reverse('post', args=[post.id])

    data = {'body': 'Comment one'}

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == url + '#comment-' + str(Comment.objects.first().id)
    assert Comment.objects.first().body == 'Comment one'


# Test PostEdit class view

def test_post_edit_view_get_request(client, create_post_page_edit_context):
    post = create_post_page_edit_context['post']
    response = client.get(reverse('edit-post', args=[post.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, 'core/post_form.html')


def test_post_edit_view_post_request(client, create_post_page_edit_context):
    post = create_post_page_edit_context['post']
    url = reverse('edit-post', args=[post.id])

    data = {'title': 'Brand New Title', 'body': 'New Body'}

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('post', args=[post.id])
    assert Post.objects.get(id=post.id).title == 'Brand New Title'


def test_post_edit_view_not_post_author(client, create_user_and_login):
    post = mixer.blend(Post)
    response = client.get(reverse('edit-post', args=[post.id]))
    assert response.status_code == 403


# Test delete_post view

def test_delete_post_view_get_request(client, create_post_page_edit_context):
    post = create_post_page_edit_context['post']
    url = reverse('delete-post', args=[post.id])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed('delete.html')
    assert response.context['object'] == post


def test_delete_post_view_post_request(client, create_post_page_edit_context):
    post = create_post_page_edit_context['post']
    url = reverse('delete-post', args=[post.id])
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert not Post.objects.filter(id=post.id).exists()


def test_delete_post_view_not_logged_in(client):
    post = mixer.blend(Post)
    url = reverse('delete-post', args=[post.id])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


def test_delete_post_view_not_author(client, create_user_and_login):
    post = mixer.blend(Post)
    response = client.get(reverse('delete-post', args=[post.id]))
    assert response.status_code == 403


# -------------------Test comment views------------------------

# Test reply_comment view

def test_reply_view(client, create_user_and_login):
    comment = mixer.blend(Comment)
    post = comment.post
    url = reverse('reply')
    data = {
        'parent': comment.id,
        'post': post.id,
        'body': 'Reply Comment'
    }
    response = client.post(url, data)

    assert response.status_code == 302

    reply = Comment.objects.get(body='Reply Comment')

    assert response.url == reverse('post', args=[post.id]) + '#comment-' + str(reply.id)
    assert reply.body == 'Reply Comment'
    assert reply.parent == comment
    assert reply.post == comment.post


def test_reply_page_not_logged_in(client):
    response = client.get(reverse('reply'))
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('reply')


# Test delete_comment view

def test_delete_comment_view_get_request(client, create_user_and_login):
    user = create_user_and_login
    comment = mixer.blend(Comment, user=user)
    url = reverse('delete-comment', args=[comment.id])
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed('delete.html')
    assert response.context['object'] == comment


def test_delete_comment_view_post_request(client, create_user_and_login):
    user = create_user_and_login
    comment = mixer.blend(Comment, user=user)
    post = comment.post
    url = reverse('delete-comment', args=[comment.id])
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('post', args=[post.id])
    assert not Comment.objects.filter(id=post.id).exists()


def test_delete_comment_view_not_logged_in(client):
    comment = mixer.blend(Comment)
    url = reverse('delete-comment', args=[comment.id])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + url


def test_delete_comment_view_not_author(client, create_user_and_login):
    comment = mixer.blend(Comment)
    url = reverse('delete-comment', args=[comment.id])
    response = client.get(url)
    assert response.status_code == 403
