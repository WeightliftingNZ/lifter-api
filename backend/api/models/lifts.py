from config.settings.base import HASHID_FIELD_SALT
from django.core.validators import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from .utils import (
    DEFAULT_LIFT_STATUS,
    LIFT_STATUS,
    WEIGHT_CATEGORIES,
    key_sort_lifts,
    ranking_suffixer,
)


class Lift(models.Model):
    """Lift."""

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
        max_length=5, choices=WEIGHT_CATEGORIES, blank=True
    )
    # TODO: if `team` is "GUEST", then lifter is a guest
    team = models.CharField(max_length=20, blank=True, default="IND")

    # lifts fields
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

    class Meta:
        """Meta."""

        ordering = ["weight_category", "lottery_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "lottery_number", "session_number"],
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
    def snatches(self):
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
    def cnjs(self):
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
    def best_snatch_weight(self):
        """Best snatch weight returned."""
        snatches = [
            # (if lift was made, weight of lift)
            ("1st", self.snatch_first, self.snatch_first_weight),
            ("2nd", self.snatch_second, self.snatch_second_weight),
            ("3rd", self.snatch_third, self.snatch_third_weight),
        ]
        best_snatch = 0
        best_snatch_attempt = ""
        for snatch_attempt, snatch_made, snatch_weight in snatches:
            if snatch_made == "LIFT" and snatch_weight > best_snatch:
                best_snatch = snatch_weight
                best_snatch_attempt = snatch_attempt
        return best_snatch_attempt, best_snatch

    @property
    def best_cnj_weight(self):
        """Best clean and jerk returned."""
        cnjs = [
            ("1st", self.cnj_first, self.cnj_first_weight),
            ("2nd", self.cnj_second, self.cnj_second_weight),
            ("3rd", self.cnj_third, self.cnj_third_weight),
        ]

        best_cnj = 0
        best_cnj_attempt = ""
        for cnj_attempt, cnj_made, cnj_weight in cnjs:
            if cnj_made == "LIFT" and cnj_weight > best_cnj:
                best_cnj = cnj_weight
                best_cnj_attempt = cnj_attempt
        return best_cnj_attempt, best_cnj

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

    #
    # age
    #
    # TODO: write tests to determine placing as well as juniors etc
    @property
    def years_from_birth(self) -> int:
        """Calculate year from birth at time of competition."""
        # TODO: is the start of the compeitition used to determine the year or
        # time of the session?
        return self.competition.date_start.year - self.yearborn

    @property
    def is_youth(self) -> bool:
        """13-17 years."""
        return self.years_from_birth >= 13 and self.years_from_birth <= 17

    @property
    def is_junior(self) -> bool:
        """15-20 years."""
        return self.years_from_birth >= 15 and self.years_from_birth <= 20

    @property
    def is_senior(self) -> bool:
        """15+ years."""
        return self.years_from_birth > 15

    @property
    def is_master(self) -> bool:
        """35+ years."""
        return self.years_from_birth > 35

    @cached_property
    # TODO: placings for junior, senior etc
    def placing(self) -> str:
        """Determine placing of the athlete from weightclass."""
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
        sorted_lifts = sorted(lifts, key=key_sort_lifts)
        sorted_lifts_ids = [lift["reference_id"] for lift in sorted_lifts]
        return ranking_suffixer(sorted_lifts_ids.index(self.reference_id) + 1)

    def clean(self, *args, **kwargs):
        """Customise validation.

        If a lift is made, then the next lift has to be an increment
        """
        DICT_PLACING = {1: "1st", 2: "2nd", 3: "3rd"}
        snatches = self.snatches
        lst_snatches = list(snatches.values())

        for i, snatch in enumerate(lst_snatches):
            # if lift is made
            # the next weight must be greater than previous, unless it's DNA
            if i < 2:
                if (
                    snatch["lift_status"] == "LIFT"
                    and lst_snatches[i + 1]["lift_status"] != "DNA"
                    and snatch["weight"] >= lst_snatches[i + 1]["weight"]
                ):
                    # if lift is made
                    # current weight must be greater than previous
                    raise ValidationError(
                        _(
                            f"{DICT_PLACING[i+2]} snatch cannot be lower or same than previous lift if a good lift."
                        )
                    )
                if (
                    snatch["lift_status"] == "NOLIFT"
                    and lst_snatches[i + 1]["lift_status"] != "DNA"
                    and snatch["weight"] > lst_snatches[i + 1]["weight"]
                ):
                    # if lift is not made or not attempted
                    # current weight must be same or greater than previous
                    raise ValidationError(
                        _(
                            f"{DICT_PLACING[i+2]} snatch cannot be less than previous lift."
                        )
                    )

        cnjs = self.cnjs
        lst_cnjs = list(cnjs.values())

        for i, cnj in enumerate(lst_cnjs):
            if i < 2:
                if (
                    cnj["lift_status"] == "LIFT"
                    and lst_cnjs[i + 1]["lift_status"] != "DNA"
                    and cnj["weight"] >= lst_cnjs[i + 1]["weight"]
                ):
                    raise ValidationError(
                        _(
                            f"{DICT_PLACING[i+2]} clean and jerk cannot be lower or same than previous lift if a good lift."
                        )
                    )
                if (
                    cnj["lift_status"] == "LIFT"
                    and lst_cnjs[i + 1]["lift_status"] != "DNA"
                    and cnj["weight"] > lst_cnjs[i + 1]["weight"]
                ):
                    raise ValidationError(
                        _(
                            f"{DICT_PLACING[i+2]} clean and jerk cannot be less than previous lift."
                        )
                    )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """__str__."""
        return f"{self.athlete} - {self.competition} {self.competition.date_start.year}"
