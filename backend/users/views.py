from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, viewsets

from .models import CustomUser
from .serializers import UserDetailsSerializer


@extend_schema_view(
    list=extend_schema(parameters=[OpenApiParameter("id")], exclude=True)
)
class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer_class(self):
        return UserDetailsSerializer
