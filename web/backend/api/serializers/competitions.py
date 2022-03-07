from rest_framework import serializers

from api.models import Competition
from .lifts import LiftSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )

    class Meta:
        model = Competition
        fields = (
            "url",
            "date_start",
            "date_end",
            "location",
            "competition_name",
        )


class CompetitionDetailSerializer(CompetitionSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + ("lift_set",)
