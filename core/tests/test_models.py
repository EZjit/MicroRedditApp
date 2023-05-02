import pytest
from mixer.backend.django import mixer
from django.db import IntegrityError
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from django.urls import reverse
from core.models import Community, Post, Comment



pytestmark = pytest.mark.django_db


@pytest.fixture
def community_instance():
    return mixer.blend(Community, name='Community', description='Bla-bla-bla')


@pytest.fixture
def post_instance():
    return mixer.blend(Post, title='Post', body='Bla-bla-bla')


@pytest.fixture
def comment_instance():
    return mixer.blend(Comment, body='Comment', parent=None)


# --------------------Test Community model------------------------

# Test creating valid instance

def test_create_community(community_instance):
    community = community_instance
    assert community.name == 'Community'
    assert community.description == 'Bla-bla-bla'
    assert community.created_at is not None


# Testing methods

def test_community_str(community_instance):
    assert str(community_instance) == 'Community'


# Testing field validations and constraints

@pytest.mark.parametrize('name, description, field, message', [
    ('', 'Description', 'name', 'cannot be blank'),  # Community name cannot be blank
    ('a' * 201, 'Description', 'name', 'has at most 25 characters'),  # Maximum name length is 25
    ('a' * 2, 'Description', 'name', 'has at least 3 characters'),  # Minimum name length is 3
    ('Name', '', 'description', 'cannot be blank'),  # Description cannot be blank
    ])
def test_community_fields_validation(name, description, field, message):
    community = Community(name=name, description=description)
    with pytest.raises(ValidationError) as e:
        community.full_clean()
    assert field in str(e.value)
    assert message in str(e.value)


def test_community_name_unique(community_instance):
    community = community_instance
    with pytest.raises(IntegrityError) as e:
        mixer.blend(Community, name=community.name)
    assert 'duplicate key value violates unique constraint' in str(e.value)


# ------------------------Test Post model--------------------------

# Test creating valid instance

def test_create_post(post_instance):
    post = post_instance
    assert post.title == 'Post'
    assert post.body == 'Bla-bla-bla'
    assert post.created_at is not None
    assert post.updated_at is not None


# Test field validations and constraints

@pytest.mark.parametrize(
    'title, body, field, message', [
        ('', 'Body', 'title', 'cannot be blank'),  # Title cannot be blank
        ('Ti', 'Body', 'title', 'has at least 3 characters'),  # Title minimum length is 3
        ('Valid Title', '', 'body', 'cannot be blank'),  # Body cannot be blank
    ])
def test_post_fields_validation(title, body, field, message):
    post = mixer.blend(Post, title=title, body=body)
    with pytest.raises(ValidationError) as e:
        post.full_clean()
    assert field in str(e.value)
    assert message in str(e.value)


# Testing methods

def test_post_str(post_instance):
    assert str(post_instance) == 'Post'


def test_get_absolute_url(post_instance):
    url = reverse('post', kwargs={'id': post_instance.id})
    assert post_instance.get_absolute_url() == url


def test_get_post_comments():
    post = mixer.blend(Post)
    top_level_comment = mixer.blend(Comment, post=post, parent=None)

    # Creating nested comment to ensure method returns only top-level comments
    mixer.blend(Comment, post=post, parent=top_level_comment)

    assert list(post.get_comments()) == [top_level_comment]


def test_get_post_comments_if_no_comments():
    post = mixer.blend(Post)
    assert list(post.get_comments()) == []


# ---------------------Test Comment model----------------------

# Test creating valid instance

def test_create_comment(comment_instance):
    comment = comment_instance
    assert comment.body == 'Comment'
    assert comment.created_at is not None


def test_create_nested_comments(comment_instance):
    top_level_comment = comment_instance
    nested_comment = mixer.blend(Comment, parent=top_level_comment)
    assert nested_comment.body
    assert nested_comment.parent == top_level_comment


# Testing methods

def test_comment_str(comment_instance):
    assert str(comment_instance) == comment_instance.body[:20]


def test_get_comment_comments(comment_instance):
    top_level_comment = comment_instance

    # Creating nested level 1 and level 2 comment to ensure method returns only
    # direct childrens of comment instance
    level_1_comment = mixer.blend(Comment, post=top_level_comment.post,
                                  parent=top_level_comment)
    level_2_comment = mixer.blend(Comment, post=top_level_comment.post,
                                  parent=level_1_comment)

    assert list(top_level_comment.get_comments()) == [level_1_comment]
    assert list(level_1_comment.get_comments()) == [level_2_comment]
    assert list(level_2_comment.get_comments()) == []
