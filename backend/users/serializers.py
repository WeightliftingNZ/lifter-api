from dj_rest_auth.serializers import (
    UserDetailsSerializer as RestUserDetailsSerializer,
)
from drf_spectacular.utils import extend_schema_serializer
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers


@extend_schema_serializer(
    exclude_fields=[
        "reference_id",
    ]
)
class UserDetailsSerializer(RestUserDetailsSerializer):
    pk = serializers.PrimaryKeyRelatedField(  # type: ignore
        pk_field=HashidSerializerCharField(
            source_field="users.CustomUser.reference_id"
        ),
        read_only=True,
    )

    class Meta(RestUserDetailsSerializer.Meta):
        fields = RestUserDetailsSerializer.Meta.fields + ("pk",)
