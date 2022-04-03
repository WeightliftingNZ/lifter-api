from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema_serializer,
)
from rest_framework import serializers

from .models import CustomUser


@extend_schema_serializer(exclude_fields=("pk",))
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
