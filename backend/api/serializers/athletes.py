from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_serializer,
)
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Athlete

from .lifts import LiftSerializer


@extend_schema_serializer(
    exclude_fields=("url",),
    examples=[
        OpenApiExample(
            "Response Example",
            summary="summary",
            description="This returns the details of the Athlete",
            value={
                "reference_id": "MzaeWrE",
                "full_name": "SEKONE-FRASER, Douglas",
                "first_name": "Douglas",
                "last_name": "Sekone-Fraser",
                "yearborn": 1991,
                "is_youth": False,
                "is_junior": False,
                "is_senior": True,
                "is_master": False,
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
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


# @extend_schema_serializer(exclude_fields=("reference_id", "full_name"))
class AthleteDetailSerializer(AthleteSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(AthleteSerializer.Meta):
        fields = AthleteSerializer.Meta.fields + ("lift_set",)
