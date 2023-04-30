from django.contrib import admin
from . import models


@admin.register(models.Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'community', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'community']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user', 'body']
