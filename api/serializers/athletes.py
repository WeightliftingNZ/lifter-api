from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema_serializer,
)
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Athlete

from .lifts import LiftSerializer


# TODO: schema
@extend_schema_serializer(exclude_fields=("id",))
class AthleteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="athletes-detail", read_only=True
    )

    reference_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Athlete.reference_id",
        ),
        read_only=True,
    )

    class Meta:
        model = Athlete
        fields = (
            "reference_id",
            "url",
            "full_name",
            "first_name",
            "last_name",
            "yearborn",
            "is_youth",
            "is_junior",
            "is_senior",
            "is_master",
        )


class AthleteDetailSerializer(AthleteSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(AthleteSerializer.Meta):
        fields = AthleteSerializer.Meta.fields + ("lift_set",)
