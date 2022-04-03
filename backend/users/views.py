from rest_framework import viewsets

from .models import CustomUser
from .serializers import UserDetailsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Users"""

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_class(self):
        return UserDetailsSerializer
