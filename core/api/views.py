from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from core.models import Post, Community, Comment
from . import serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = PageNumberPagination


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = serializers.CommunitySerializer
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = PageNumberPagination
