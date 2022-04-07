from dj_rest_auth.serializers import UserDetailsSerializer
from drf_spectacular.utils import (  # OpenApiExample,; OpenApiParameter,
    extend_schema_serializer,
)
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers


@extend_schema_serializer(exclude_fields=("reference_id",))
class UserDetailsSerializer(UserDetailsSerializer):
    pk = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="users.CustomUser.reference_id"
        ),
        read_only=True,
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("pk",)
