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
    competition_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_last_edited = serializers.SerializerMethodField(read_only=True)

    def get_lifts_count(self, competition) -> int:
        """Provide count of all lifts in a competition."""
        return Lift.objects.filter(competition=competition).count()

    def get_random_lifts(self, competition):
        """Provide random lifts within the competition."""

        def _randomize(sex):
            lifts = list(
                Lift.objects.filter(competition=competition).filter(
                    weight_category__startswith=sex
                )
            )
            if len(lifts) == 0:
                return []
            k_sample = 2
            if len(lifts) < k_sample:
                k_sample = len(lifts)
            return random.sample(lifts, k=k_sample)

        w_lifts = _randomize(sex="W")
        m_lifts = _randomize(sex="M")

        return LiftSerializer(
            w_lifts + m_lifts,
            many=True,
            read_only=True,
            context=self.context,
        ).data

    def get_competition_last_edited(self, competition):
        """Provide when competition was last edited."""
        if competition.history_record.all():
            return competition.history_record.latest().history_date

    def get_lift_last_edited(self, competition):
        """Provide when lifts for a competition were last edited."""
        lifts = Lift.history_record.filter(competition=competition)
        if lifts:
            return lifts.latest().history_date

    class Meta:
        model = Competition
        fields = [
            "url",
            "reference_id",
            "name",
            "location",
            "date_start",
            "date_end",
            "competition_last_edited",
            "lift_last_edited",
            "lifts_count",
            "random_lifts",
        ]


class CompetitionDetailSerializer(CompetitionSerializer):
    lift_set = serializers.SerializerMethodField(read_only=True)

    def get_lift_set(self, competition):
        """Require to ensure lifts are in custom order due to weight classes."""
        query = Lift.objects.ordered_filter(**{"competition": competition})
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + [
            "lift_set",
        ]
