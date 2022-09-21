"""Competition Serializer."""

import random

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Competition, Lift
from api.serializers.lifts import LiftSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )
    reference_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        pk_field=HashidSerializerCharField(
            source_field="api.Competition.reference_id",
        ),
        read_only=True,
    )
    lifts_count = serializers.SerializerMethodField(read_only=True)
    random_lifts = serializers.SerializerMethodField(read_only=True)

    def get_lifts_count(self, competition) -> int:
        return Lift.objects.filter(competition=competition).count()

    def get_random_lifts(self, competition) -> list:
        lifts = list(Lift.objects.filter(competition=competition))
        if len(lifts) == 0:
            return []
        sample = 3
        if len(lifts) < 3:
            sample = len(lifts)
        return LiftSerializer(
            random.sample(lifts, k=sample),
            many=True,
            read_only=True,
            context=self.context,
        ).data

    class Meta:
        model = Competition
        fields = [
            "url",
            "reference_id",
            "date_start",
            "date_end",
            "location",
            "name",
            "lifts_count",
            "random_lifts",
        ]


class CompetitionDetailSerializer(CompetitionSerializer):
    lift_set = serializers.SerializerMethodField(read_only=True)

    def get_lift_set(self, competition):
        """Required to ensure lifts are in custom order due to weight classes."""
        query = Lift.objects.ordered_filter(**{"competition": competition})
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + [
            "lift_set",
        ]
