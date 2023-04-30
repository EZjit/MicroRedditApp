from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse
from users.models import User


class Community(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(3)],
        )
    description = models.TextField(blank=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name='Choose a community',
        )
    title = models.CharField(
        max_length=80,
        blank=False,
        validators=[MinLengthValidator(3)],
        )
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id})

    def get_comments(self):
        return self.comments.filter(parent=None)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children')
    body = models.TextField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body[:20]

    def get_comments(self):
        return Comment.objects.filter(parent=self)
