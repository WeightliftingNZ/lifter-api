"""Competition Serializer."""

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Competition, Lift
from api.serializers.lifts import LiftSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    """Competition Serializer for list view."""

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
    best_lifts = serializers.SerializerMethodField(read_only=True)

    def get_lifts_count(self, competition) -> int:
        """Provide count of all lifts in a competition."""
        return Lift.objects.filter(competition=competition).count()

    def get_best_lifts(self, competition):
        """Provide the best lift for the competition, equal men's and women's."""
        women_lifts = Lift.objects.filter(
            competition=competition, weight_category__startswith="W"
        )
        men_lifts = Lift.objects.filter(
            competition=competition, weight_category__startswith="M"
        )

        def _best_lift(lifts) -> list:
            NUMBER_BEST = 2
            if lifts.count() == 0:
                return []
            if lifts.count() < NUMBER_BEST:
                NUMBER_BEST = lifts.count()
            lifts = list(lifts)
            lifts.sort(key=lambda lift: lift.sinclair, reverse=True)
            return lifts[:NUMBER_BEST]

        return LiftSerializer(
            _best_lift(women_lifts) + _best_lift(men_lifts),
            many=True,
            read_only=True,
            context=self.context,
        ).data

    class Meta:
        """Settings for the serializer."""

        model = Competition
        fields = [
            "url",
            "reference_id",
            "name",
            "location",
            "date_start",
            "date_end",
            "lifts_count",
            "best_lifts",
        ]


class CompetitionDetailSerializer(CompetitionSerializer):
    """Serializer for the competition detail view."""

    competition_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_set = serializers.SerializerMethodField(read_only=True)

    def get_competition_last_edited(self, competition):
        """Provide when competition was last edited."""
        if competition.history_record.all():
            return competition.history_record.latest().history_date

    def get_lift_last_edited(self, competition):
        """Provide when lifts for a competition were last edited."""
        lifts = Lift.history_record.filter(competition=competition)
        if lifts:
            return lifts.latest().history_date

    def get_lift_set(self, competition):
        """Require to ensure lifts are in custom order due to weight classes."""
        query = Lift.objects.ordered_filter(**{"competition": competition})
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    class Meta(CompetitionSerializer.Meta):
        """Setting for the serializer."""

        fields = CompetitionSerializer.Meta.fields + [
            "competition_last_edited",
            "lift_last_edited",
            "lift_set",
        ]
