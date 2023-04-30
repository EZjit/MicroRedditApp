from rest_framework.serializers import ModelSerializer
from core.models import Post, Community, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'