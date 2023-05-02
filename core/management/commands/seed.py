import logging

from django.core.management.base import BaseCommand

from core.models import Community, Post, Comment
from users.models import User

# python manage.py seed --mode=refresh
""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

# python manage.py seed --mode=clear
""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the communities, posts and objects"""
    logging.info("Delete Communities Instances")
    Community.objects.all().delete()
    User.objects.all().delete()


def create_user(number: int):
    """Creates a user"""
    logging.info("Creating user")

    user = User(
        username=f'default{number}',
        email=f'test{number}@example.com',
        password='9iJ8Uh7yG'
    )
    user.save()
    logging.info(f"{user} user created.")
    return user


def create_community(number: int):
    """Creates a community object"""
    logging.info("Creating community")

    community = Community(
        name=f'Community number {number}',
        description=f'Some description of the community number {number} bla-bla-bla'
    )
    community.save()
    logging.info(f"{community} community created.")
    return community


def create_post(number: int):
    """Creates a post object"""
    logging.info("Creating post")

    post = Post(
        user=User.objects.order_by('?').first(),
        community=Community.objects.order_by('?').first(),
        title=f'Post number {number}',
        body=f'Description of post number {number}. Bla bla bla bla bla',
    )
    post.save()
    logging.info(f'"{post}" post created.')
    return post


def create_comment(number: int, top_level: bool = False):
    """Creates a comment object"""
    logging.info("Creating comment")
    parent = Comment.objects.order_by('?').first() if not top_level else None
    post = parent.post if parent else Post.objects.order_by('?').first()

    comment = Comment(
        user=User.objects.order_by('?').first(),
        parent=parent,
        post=post,
        body='',
    )

    level = get_level(comment)
    comment.body = f'Comment number {number} on level {level}'
    comment.save()
    logging.info(f'"{comment}" comment created.')
    return comment


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Seeding db
    for number in range(1, 8):
        create_community(number)

    for number in range(1, 11):
        create_user(number)

    for number in range(1, 101):
        create_post(number)

    for number in range(1, 1001):
        create_comment(number, top_level=True)

    for number in range(1, 10001):
        create_comment(number)


# Utility methods
def get_level(comment):
    level = 0
    while comment.parent:
        level += 1
        comment = comment.parent
    return level
