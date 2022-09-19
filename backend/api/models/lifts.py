"""Lift model."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from hashid_field import HashidAutoField

from api.models.utils.helpers import calculate_sinclair
from config.settings import HASHID_FIELD_SALT

from .managers import LiftManager
from .utils import (
    CURRENT_FEMALE_WEIGHT_CATEGORIES,
    CURRENT_MALE_WEIGHT_CATEGORIES,
    DEFAULT_LIFT_STATUS,
    LIFT_STATUS,
    OLD_1998_2018_FEMALE_WEIGHT_CATEGORIES,
    OLD_1998_2018_MALE_WEIGHT_CATEGORIES,
    age_category,
    best_lift,
    ranking_suffixer,
    validate_attempts,
)
from .utils.types import AgeCategories, LiftT

CURRENT_WEIGHT_CATEGORIES = (
    CURRENT_FEMALE_WEIGHT_CATEGORIES + CURRENT_MALE_WEIGHT_CATEGORIES
)

OLD_WEIGHT_CATEGORIES = (
    OLD_1998_2018_FEMALE_WEIGHT_CATEGORIES
    + OLD_1998_2018_MALE_WEIGHT_CATEGORIES
)

ALL_WEIGHT_CATEGORIES = CURRENT_WEIGHT_CATEGORIES + OLD_WEIGHT_CATEGORIES


# TODO: Not using this model
class Session(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"sessionmodel_reference_id_{HASHID_FIELD_SALT}"
    )
    competition = models.ForeignKey(
        "api.Competition", on_delete=models.CASCADE
    )
    number = models.IntegerField(blank=True)
    date_time = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "number"],
                name="competition_number_unique_combination",
            ),
        ]


# TODO: Not using this model
class Team(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"teammodel_reference_id_{HASHID_FIELD_SALT}"
    )
    team = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=128, blank=True)


class Lift(models.Model):
    """Lift model."""

    # key fields
    reference_id = HashidAutoField(
        primary_key=True, salt=f"liftmodel_reference_id_{HASHID_FIELD_SALT}"
    )
    competition = models.ForeignKey(
        "api.Competition", on_delete=models.CASCADE
    )
    athlete = models.ForeignKey("api.Athlete", on_delete=models.CASCADE)

    # other fields
    session_number = models.IntegerField(null=True)
    lottery_number = models.IntegerField(blank=True)
    bodyweight = models.DecimalField(
        blank=True, max_digits=5, decimal_places=2
    )
    weight_category = models.CharField(
        max_length=5, choices=ALL_WEIGHT_CATEGORIES, blank=True
    )
    # TODO: if `team` is "GUEST", then lifter is a guest
    team = models.CharField(max_length=128, blank=True, default="IND")

    # lifts fields
    # snatches
    snatch_first = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    snatch_first_weight = models.IntegerField(blank=True, default=0)
    snatch_second = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    snatch_second_weight = models.IntegerField(blank=True, default=0)
    snatch_third = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    snatch_third_weight = models.IntegerField(blank=True, default=0)

    # cnj
    cnj_first = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    cnj_first_weight = models.IntegerField(blank=True, default=0)
    cnj_second = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    cnj_second_weight = models.IntegerField(blank=True, default=0)
    cnj_third = models.CharField(
        max_length=6,
        choices=LIFT_STATUS,
        blank=True,
        default=DEFAULT_LIFT_STATUS,
    )
    cnj_third_weight = models.IntegerField(blank=True, default=0)

    objects = LiftManager()

    class Meta:
        ordering = ["weight_category", "lottery_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "lottery_number", "weight_category"],
                name="session_lottery_unique_combination",
            ),
            models.UniqueConstraint(
                fields=["competition", "athlete"],
                name="competition_athlete_unique_combination",
            ),
        ]

    #
    # custom fields
    #
    # lifts
    #
    @property
    def snatches(self) -> dict[str, LiftT]:
        """Snatches custom field."""
        return {
            "1st": {
                "lift_status": self.snatch_first,
                "weight": self.snatch_first_weight,
            },
            "2nd": {
                "lift_status": self.snatch_second,
                "weight": self.snatch_second_weight,
            },
            "3rd": {
                "lift_status": self.snatch_third,
                "weight": self.snatch_third_weight,
            },
        }

    @property
    def cnjs(self) -> dict[str, LiftT]:
        """Clean and Jerk custom field."""
        return {
            "1st": {
                "lift_status": self.cnj_first,
                "weight": self.cnj_first_weight,
            },
            "2nd": {
                "lift_status": self.cnj_second,
                "weight": self.cnj_second_weight,
            },
            "3rd": {
                "lift_status": self.cnj_third,
                "weight": self.cnj_third_weight,
            },
        }

    @property
    def best_snatch_weight(self) -> tuple[str, int]:
        """Best snatch weight returned."""
        return best_lift(self.snatches)

    @property
    def best_cnj_weight(self) -> tuple[str, int]:
        """Best clean and jerk returned."""
        return best_lift(self.cnjs)

    @property
    def total_lifted(self) -> int:
        """Calculate total."""
        total_lifted = 0
        snatch_lifts = [
            self.snatch_first,
            self.snatch_second,
            self.snatch_third,
        ]
        cnj_lifts = [
            self.cnj_first,
            self.cnj_second,
            self.cnj_third,
        ]
        # must have at least a snatch lift and cnj to total
        snatch_made = any([lift == "LIFT" for lift in snatch_lifts])
        cnj_made = any([lift == "LIFT" for lift in cnj_lifts])
        if all([snatch_made, cnj_made]):
            total_lifted = self.best_snatch_weight[1] + self.best_cnj_weight[1]
        return total_lifted

    @property
    def age_categories(self) -> AgeCategories:
        """Age category of the athlete at the time of the lift."""
        return age_category(
            yearborn=self.athlete.yearborn,
            competition_year=self.competition.date_start.year,
        )

    @property
    def sinclair(self) -> Decimal:
        """Calculate sinclair for a lift."""
        return calculate_sinclair(
            bodyweight=self.bodyweight,
            total_lifted=self.total_lifted,
            weight_category=self.weight_category,
            yearborn=self.athlete.yearborn,
            lift_year=self.competition.date_start.year,
        )

    @cached_property
    # TODO: placings for junior, senior etc
    def placing(self):
        """Determine placing of the athlete from weightclass.

        How placing is determined in weightlifting:
        1. Best total
        - If totals are tied, then we need to determine who achieved the total
        first.
        2. Lowest clean and jerk
        3. Least number of attempts
        4. Lowest lottery number
        """
        if self.total_lifted == 0:
            return "-"
        query = Lift.objects.filter(
            competition=self.competition, weight_category=self.weight_category
        )
        lifts = [
            {
                "reference_id": q.reference_id,
                "best_cnj_weight": q.best_cnj_weight,
                "total_lifted": q.total_lifted,
                "lottery_number": q.lottery_number,
            }
            for q in query
            if q.total_lifted > 0  # ensures sorted lifts have a total
        ]
        sorted_lifts = sorted(
            lifts,
            key=lambda x: (
                -x["total_lifted"],
                x["best_cnj_weight"][1],
                x["best_cnj_weight"][0],
                x["lottery_number"],
            ),
        )
        sorted_lifts_ids = [lift["reference_id"] for lift in sorted_lifts]
        return ranking_suffixer(sorted_lifts_ids.index(self.reference_id) + 1)

    def clean(self, *args, **kwargs):
        """Customise validation.

        0. Validation attempts to ensure they are increasing depending on the
        current lift status.
        1. Weightclasses are relevant to the date of the competition.
        """
        errors = []
        # 0. lift validation
        errors.extend(
            validate_attempts(attempts=self.snatches, lift_type="snatch")
        )
        errors.extend(
            validate_attempts(attempts=self.cnjs, lift_type="clean and jerk")
        )

        # 1. Weightclass validation
        # CATEGORY is list of tuples e.g. `[..., ('M102+', 'M102+'), ...]`
        if (
            self.competition.date_start.year >= 2018
            and self.weight_category
            not in (w[0] for w in CURRENT_WEIGHT_CATEGORIES)
        ) or (
            self.competition.date_start.year <= 2018
            and self.weight_category
            not in (w[0] for w in OLD_WEIGHT_CATEGORIES)
        ):
            errors.append("Weightclass from wrong era.")
        if len(errors) > 0:
            error_msg = "\n".join(errors)
            raise ValidationError(
                "%(error_msg)s",
                code="Invalid Attempt",
                params={
                    "error_msg": error_msg,
                },
            )

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Necessary to enact custom validation in `clean()` method."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """__str__."""
        return f"{self.athlete} - {self.competition} {self.competition.date_start.year}"
