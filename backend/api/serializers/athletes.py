"""Athete Serializers."""

from datetime import datetime

from django.db.models import F
from django.db.models.functions import ExtractYear
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Athlete, Lift

from .lifts import LiftSerializer


class AthleteSerializer(serializers.ModelSerializer):
    """Athlete Serialzier."""

    url = serializers.HyperlinkedIdentityField(
        view_name="athletes-detail", read_only=True
    )
    reference_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        pk_field=HashidSerializerCharField(
            source_field="api.Athlete.reference_id",
        ),
        read_only=True,
    )
    lifts_count = serializers.SerializerMethodField(read_only=True)
    recent_lift = serializers.SerializerMethodField(read_only=True)
    current_grade = serializers.SerializerMethodField(read_only=True)
    athlete_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_last_edited = serializers.SerializerMethodField(read_only=True)

    def get_lifts_count(self, athlete):
        """Provide count of lifts by athlete."""
        return Lift.objects.filter(athlete=athlete).count()

    def get_current_grade(self, athlete):
        """Provide grade of the lift by the athlete."""
        query = (
            Lift.objects.annotate(
                competition_year=ExtractYear(F("competition__date_start"))
            )
            .filter(athlete=athlete)
            .filter(competition_year=datetime.now().year)
        )
        if len(query) == 0:
            return None
        SORT = ("Elite", "International", "A", "B", "C", "D", "E", None)
        grades = [(lift.grade, SORT.index(lift.grade)) for lift in query]
        best_grade = sorted(grades, key=lambda x: x[1])
        return best_grade[0][0]

    def get_recent_lift(self, athlete):
        """Provide most recent lift for athlete."""
        query = Lift.objects.filter(athlete=athlete).order_by(
            "-competition__date_start"
        )[:1]
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    def get_athlete_last_edited(self, athlete):
        """Provide when athlete was last edited."""
        if athlete.history_record.all():
            return athlete.history_record.latest().history_date

    def get_lift_last_edited(self, athlete):
        """Provide when lifts for an athlete was last edited."""
        lifts = Lift.history_record.filter(athlete=athlete)
        if lifts:
            return lifts.latest().history_date

    class Meta:
        """Athelte serializer settings."""

        model = Athlete
        fields = [
            "reference_id",
            "url",
            "full_name",
            "first_name",
            "last_name",
            "yearborn",
            "athlete_last_edited",
            "lift_last_edited",
            "current_grade",
            "age_categories",
            "recent_lift",
            "lifts_count",
        ]


class AthleteDetailSerializer(AthleteSerializer):
    """Detail Serializer for Athlete."""

    lift_set = serializers.SerializerMethodField(read_only=True)

    def get_lift_set(self, athlete):
        """Obtain all lifts by this athlete."""
        query = Lift.objects.filter(athlete=athlete).order_by(
            "-competition__date_start"
        )
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    class Meta(AthleteSerializer.Meta):
        """Serializer settings."""

        fields = AthleteSerializer.Meta.fields + [
            "lift_set",
        ]
