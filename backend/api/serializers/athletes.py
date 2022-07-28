"""Athete Serializers."""

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Athlete

from .lifts import LiftSerializer


class AthleteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="athletes-detail", read_only=True
    )

    reference_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        pk_field=HashidSerializerCharField(
            source_field="api.Athlete.reference_id",
        ),
        read_only=True,
    )

    class Meta:
        model = Athlete
        fields = [
            "reference_id",
            "url",
            "full_name",
            "first_name",
            "last_name",
            "yearborn",
            "age_categories",
        ]


class AthleteDetailSerializer(AthleteSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(AthleteSerializer.Meta):
        fields = AthleteSerializer.Meta.fields + [
            "lift_set",
        ]
