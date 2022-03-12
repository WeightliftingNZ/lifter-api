from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Competition
from .lifts import LiftSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )
    reference_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Competition.reference_id",
        ),
        read_only=True,
    )

    class Meta:
        model = Competition
        fields = (
            "url",
            "reference_id",
            "date_start",
            "date_end",
            "location",
            "competition_name",
        )


class CompetitionDetailSerializer(CompetitionSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + ("lift_set",)
