from drf_spectacular.utils import (
    extend_schema_serializer,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from api.models import Athlete
from .lifts import LiftSerializer


# TODO: schema
@extend_schema_serializer(exclude_fields=("id",))
class AthleteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="athletes-detail", read_only=True
    )

    class Meta:
        model = Athlete
        fields = ("url", "first_name", "last_name", "yearborn")


class AthleteDetailSerializer(AthleteSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(AthleteSerializer.Meta):
        fields = AthleteSerializer.Meta.fields + ("lift_set",)
