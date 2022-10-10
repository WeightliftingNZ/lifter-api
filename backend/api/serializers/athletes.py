"""Athete Serializers."""

from collections import defaultdict
from datetime import datetime

from django.db.models import F
from django.db.models.functions import ExtractYear
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Athlete, Lift
from api.models.utils.constants import GRADES
from api.models.utils.types import AgeCategories
from api.serializers.lifts import LiftSerializer


class AthleteSerializer(serializers.ModelSerializer):
    """Athlete Serialzier for list views."""

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
    current_grade = serializers.SerializerMethodField(read_only=True)
    recent_lift = serializers.SerializerMethodField(read_only=True)

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
        grades = [(lift.grade, GRADES.index(lift.grade)) for lift in query]
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
            "current_grade",
            "age_categories",
            "lifts_count",
            "recent_lift",
        ]


class AthleteDetailSerializer(AthleteSerializer):
    """Athlete for retrieve views."""

    athlete_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_last_edited = serializers.SerializerMethodField(read_only=True)
    lift_set = serializers.SerializerMethodField(read_only=True)
    age_categories_competed = serializers.SerializerMethodField(read_only=True)
    weight_categories_competed = serializers.SerializerMethodField(
        read_only=True
    )
    best_lifts = serializers.SerializerMethodField(read_only=True)
    best_sinclair = serializers.SerializerMethodField(read_only=True)

    def get_athlete_last_edited(self, athlete):
        """Provide when athlete was last edited."""
        if athlete.history_record.all().exists() is False:
            return None
        return athlete.history_record.latest().history_date

    def get_lift_last_edited(self, athlete):
        """Provide when lifts for an athlete was last edited."""
        lifts = Lift.history_record.filter(athlete=athlete)
        if lifts.exists() is False:
            return None
        return lifts.latest().history_date

    def get_lift_set(self, athlete):
        """Obtain all lifts by this athlete."""
        query = (
            Lift.objects.filter(athlete=athlete)
            .select_related("athlete")
            .order_by("-competition__date_start")
        )
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    def get_age_categories_competed(self, athlete) -> AgeCategories:
        """Provide all age categories.

        This will be age categories athlete has been in for their entire \
                career. Will create dictionary with age_categories being True \
                is participated.
        """
        all_age_categories: AgeCategories = {
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
            for k, value in age_categories.items():
                if value:
                    all_age_categories[k] = value  # type: ignore
        return all_age_categories

    def get_weight_categories_competed(self, athlete):
        """Provide weight categories for an athlete."""
        lifts = Lift.objects.filter(athlete=athlete).values_list(
            "weight_category", flat=True
        )
        return set(lifts)

    def _best_lift(self, lifts, sort_key):
        best_lift = LiftSerializer(
            sorted(
                lifts,
                key=sort_key,
            )[-1],
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
        lifts = Lift.objects.filter(athlete=athlete)

        type_categories = [
            (
                "snatch",
                lambda lift: lift.best_snatch_weight[1],
                lambda x: x[1]["best_snatch_weight"][1],
            ),
            (
                "cnj",
                lambda lift: lift.best_cnj_weight[1],
                lambda x: x[1]["best_cnj_weight"][1],
            ),
            (
                "total",
                lambda lift: lift.total_lifted,
                lambda x: x[1]["total_lifted"],
            ),
        ]

        # e.g. lift_by_type_category = {}
        lift_by_type_category: dict = defaultdict(dict)
        for (
            type_category,
            sort_key,
            weight_category_sort_key,
        ) in type_categories:
            # e.g. lift_by_type_category = { "snatch": {} }
            lift_by_type_category[type_category] = defaultdict(dict)
            for age_category, is_true in age_categories.items():
                if is_true:
                    lift_by_type_category[type_category][
                        age_category
                    ] = defaultdict(dict)
                    lifts_by_age_category = []
                    for weight_category in weight_categories:
                        relevant_lifts = [
                            lift
                            for lift in lifts
                            if lift.weight_category == weight_category
                            and lift.age_categories[age_category]  # type: ignore
                        ]
                        if len(relevant_lifts) == 0:
                            break
                        lifts_by_age_category.append(
                            (
                                weight_category,
                                self._best_lift(relevant_lifts, sort_key),
                            )
                        )
                    if len(lifts_by_age_category) == 0:
                        del lift_by_type_category[type_category][age_category]
                        break
                    lifts_by_age_category.sort(key=weight_category_sort_key)
                    for weight_category, lift in lifts_by_age_category:
                        lift_by_type_category[type_category][
                            age_category
                        ].update({weight_category: lift})
        return lift_by_type_category

    def get_best_sinclair(self, athlete):
        """Provide the best total for the an athlete for weight categories."""
        age_categories = self.get_age_categories_competed(athlete=athlete)
        sinclair_by_age_categories: dict = defaultdict(dict)
        lifts = Lift.objects.filter(athlete=athlete)
        for age_category, is_true in age_categories.items():
            if is_true:
                clean_lifts = [
                    lift for lift in lifts if lift.age_categories[age_category]  # type: ignore
                ]
                if len(clean_lifts) == 0:
                    break
                sinclair_by_age_categories[age_category] = self._best_lift(
                    clean_lifts, lambda lift: lift.sinclair
                )
        return sinclair_by_age_categories

    class Meta(AthleteSerializer.Meta):
        """Serializer settings."""

        fields = AthleteSerializer.Meta.fields + [
            "age_categories_competed",
            "weight_categories_competed",
            "best_lifts",
            "best_sinclair",
            "lift_last_edited",
            "athlete_last_edited",
            "lift_last_edited",
            "athlete_last_edited",
            "lift_set",
        ]
