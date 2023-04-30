from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'date_created', 'avatar']
