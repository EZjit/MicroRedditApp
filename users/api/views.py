from rest_framework import viewsets
from users.models import User
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
