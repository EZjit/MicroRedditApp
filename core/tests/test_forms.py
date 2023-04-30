import pytest
from core.forms import CommentForm


pytestmark = pytest.mark.django_db


# Test Comment Form

@pytest.mark.parametrize('body, validity', [
    ('Comment', True),
    ('', False),  # Comment body cannot be blank
    ('a' * 201, False),  # Maximum comment length is 200
    ('a' * 200, True),
    ])
def test_comment_form(body, validity):
    form = CommentForm(data={'body': body})
    assert form.is_valid() is validity


def test_comment_body_placeholder():
    form = CommentForm(data={'body': 'Comment'})
    assert form.fields['body'].widget.attrs['placeholder'] == 'Comment here...'
