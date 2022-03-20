from typing import Dict, List, Tuple

from django.core.validators import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .utils import LIFT_STATUS, WEIGHT_CATEGORIES, ranking_suffix


class Lift(models.Model):
    reference_id = models.AutoField(primary_key=True)
    athlete = models.ForeignKey("api.Athlete", on_delete=models.CASCADE)
    competition = models.ForeignKey(
        "api.Competition", on_delete=models.CASCADE
    )
    session = models.ForeignKey("api.Session", on_delete=models.CASCADE)

    snatch_first = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True
    )
    snatch_first_weight = models.IntegerField(blank=True)
    snatch_second = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True
    )
    snatch_second_weight = models.IntegerField(blank=True)
    snatch_third = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True
    )
    snatch_third_weight = models.IntegerField(blank=True)
    cnj_first = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    cnj_first_weight = models.IntegerField(blank=True)
    cnj_second = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True
    )
    cnj_second_weight = models.IntegerField(blank=True)
    cnj_third = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    cnj_third_weight = models.IntegerField(blank=True)

    bodyweight = models.IntegerField()
    weight_category = models.CharField(
        max_length=5, choices=WEIGHT_CATEGORIES, blank=True
    )
    # create list of clubs?
    team = models.CharField(max_length=4, blank=True)
    lottery_number = models.IntegerField(blank=True)

    def clean(self, *args, **kwargs):
        # ensure athlete is not entered twice in a competition
        if Lift.objects.filter(
            competition=self.competition, athlete=self.athlete
        ).exists():
            raise ValidationError(_(f"{self.athlete} already in competition"))

        if Lift.objects.filter(
            competition=self.competition,
            session=self.session,
            lottery_number=self.lottery_number,
        ).exists():
            raise ValidationError(
                _(f"{self.lottery_number} already exists in this session")
            )

        # TODO: write the logic
        # this assumes lifts must increase but this is not the case
        # if there is a nolift then the weight does not necessarily have to go up
        # need to ensure lifts are always going up
        # snatches = [snatch for snatch in self.snatches.values()]
        # if current snatch is a make, next lift must be more
        # if not next snatch weight must be same of more
        # for current, snatch in enumerate(snatches, 1):
        #     if current < 3:
        #         if snatch["lift_status"] == "LIFT":
        #             if snatches[current]
        #             snatch[attempt + 1]

        # sorted_snatches = snatches.copy().sort()
        # if snatches != sorted_snatches:
        #     raise ValidationError(_("Snatches must be increasing with every attempt"))

        # cnjs = [self.cnj_first, self.cnj_second, self.cnj_third]
        # sorted_cnjes = cnjs.copy().sort()
        # if cnjs != sorted_cnjes:
        #     raise ValidationError(
        #         _("Clean and Jerks must be increasing with every attempt")
        #     )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def snatches(self) -> dict[str, dict[str, str]]:
        """Snatches data

        e.g. key is attempt, then another key pair to determine if lift is made and what the weight was lifted

        Returns:
            Dict[str, Dict[str, str]]: snatch data
        """
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
    def cnjs(self) -> dict[str, dict[str, str]]:
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
        """Best snatch weight returned

        Returns:
            Tuple[str, int]: what the lift "order" was best and the weight
        """
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
    def best_cnj_weight(self) -> tuple[str, str]:
        """Best clean and jerk returned

        Returns:
            Tuple[str, str]: the lift "order", and weight
        """
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
    def total_lifted(self):
        # TODO: write tests for this
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
        # you must have at least a snatch lift and cnj to total
        snatch_made = any([lift == "LIFT" for lift in snatch_lifts])
        cnj_made = any([lift == "LIFT" for lift in cnj_lifts])
        if all([snatch_made, cnj_made]):
            total_lifted = self.best_snatch_weight[1] + self.best_cnj_weight[1]
        return total_lifted

    @cached_property
    def placing(self):

        # same competition and weightclass
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
        ]
        if self.total_lifted == 0:
            return "-"

        def sort_lift_key(lift):
            keys = []
            # total
            keys.append(-lift["total_lifted"])
            # lowest cnj
            keys.append(lift["best_cnj_weight"][1])
            # least attempts
            keys.append(lift["best_cnj_weight"][0])
            # lott number
            keys.append(lift["lottery_number"])
            return tuple(keys)

        sorted_lifts = sorted(lifts, key=sort_lift_key)
        sorted_lifts_ids = [lift["reference_id"] for lift in sorted_lifts]
        return ranking_suffix(sorted_lifts_ids.index(self.reference_id) + 1)

    def __str__(self):
        return f"{self.athlete} - {self.competition} {self.competition.date_start.year}"
