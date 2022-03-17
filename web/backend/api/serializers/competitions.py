from collections import Counter

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Competition, Lift

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
    lift_count = serializers.SerializerMethodField(read_only=True)

    def get_lift_count(self, competition):
        return Lift.objects.filter(competition=competition).count()

    class Meta:
        model = Competition
        fields = (
            "url",
            "reference_id",
            "date_start",
            "date_end",
            "location",
            "competition_name",
            "lift_count",
        )


class CompetitionDetailSerializer(CompetitionSerializer):
    lift_set = LiftSerializer(many=True, read_only=True)

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + ("lift_set",)
