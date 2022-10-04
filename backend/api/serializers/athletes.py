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
    age_categories_competed = serializers.SerializerMethodField(read_only=True)
    weight_categories_competed = serializers.SerializerMethodField(
        read_only=True
    )
    best_lifts = serializers.SerializerMethodField(read_only=True)
    best_sinclair = serializers.SerializerMethodField(read_only=True)

    def get_lift_set(self, athlete):
        """Obtain all lifts by this athlete."""
        query = Lift.objects.filter(athlete=athlete).order_by(
            "-competition__date_start"
        )
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    def get_age_categories_competed(self, athlete) -> dict[str, bool]:
        """Provide all age categories.

        This will be age categories athlete has been in for their entire \
                career. Will create dictionary with age_categories being True \
                is participated.
                """
        all_age_categories = {
            "is_youth": False,
            "is_junior": False,
            "is_senior": False,
            "is_master": False,
            "is_master_35_39": False,
            "is_master_40_44": False,
            "is_master_45_49": False,
            "is_master_50_54": False,
            "is_master_55_59": False,
            "is_master_60_64": False,
            "is_master_65_69": False,
            "is_master_70": False,
        }
        for lift in Lift.objects.filter(athlete=athlete):
            age_categories = lift.age_categories
            for k, v in age_categories.items():
                if v:
                    all_age_categories[k] = v  # type: ignore
        return all_age_categories

    def get_weight_categories_competed(self, athlete) -> list[str]:
        """Provide weight categories for an athlete."""
        unique_weight_categories = []
        for lift in Lift.objects.filter(athlete=athlete):
            weight_category = lift.weight_category
            if weight_category not in unique_weight_categories:
                unique_weight_categories.append(weight_category)
        return unique_weight_categories

    def _best_lift(self, lifts, sort_key):
        if lifts.count() == 0:
            return None
        best_lift = LiftSerializer(
            sorted(lifts, key=sort_key)[-1],
            read_only=True,
            context=self.context,
        ).data
        return best_lift

    def get_best_lifts(self, athlete) -> dict:
        """Provide the best snatch for the an athlete for a given weight \
                categories."""

        age_categories = self.get_age_categories_competed(athlete=athlete)
        weight_categories = self.get_weight_categories_competed(
            athlete=athlete
        )
        order_bys = [
            ("snatch", lambda lift: lift.best_snatch_weight[1]),
            ("cnj", lambda lift: lift.best_cnj_weight[1]),
            ("total", lambda lift: lift.total_lifted),
        ]
        lift_by_age_weight_category: dict = {}
        for order_by, sort_key in order_bys:
            lift_by_age_weight_category[order_by] = {}
            for age_category, is_true in age_categories.items():
                if is_true:
                    lift_by_age_weight_category[order_by].update(
                        {age_category: {}}
                    )
                    for weight_category in weight_categories:
                        lifts = Lift.objects.filter(athlete=athlete).filter(
                            weight_category=weight_category
                        )
                        lift_by_age_weight_category[order_by][
                            age_category
                        ].update(
                            {weight_category: self._best_lift(lifts, sort_key)}
                        )
        return lift_by_age_weight_category

    def get_best_sinclair(self, athlete):
        """Provide the best total for the an athlete for weight categories."""
        age_categories = self.get_age_categories_competed(athlete=athlete)
        sinclair_by_age_categories = {}
        lifts = Lift.objects.filter(athlete=athlete)
        for age_category, is_true in age_categories.items():
            if is_true:
                sinclair_by_age_categories[age_category] = self._best_lift(
                    lifts, lambda lift: lift.sinclair
                )
        return sinclair_by_age_categories

    class Meta(AthleteSerializer.Meta):
        """Serializer settings."""

        fields = AthleteSerializer.Meta.fields + [
            "lift_set",
            "age_categories_competed",
            "weight_categories_competed",
            "best_lifts",
            "best_sinclair",
        ]
