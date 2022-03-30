from django.core.validators import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from .competitions import Competition
from .sessions import Session
from .utils import DEFAULT_LIFT_STATUS, LIFT_STATUS, WEIGHT_CATEGORIES, ranking_suffix


class Lift(models.Model):
    # key fields
    reference_id = HashidAutoField(primary_key=True)
    athlete = models.ForeignKey("api.Athlete", on_delete=models.CASCADE)
    session = models.ForeignKey("api.Session", on_delete=models.CASCADE)

    # other fields
    lottery_number = models.IntegerField(blank=True)
    bodyweight = models.IntegerField()
    weight_category = models.CharField(
        max_length=5, choices=WEIGHT_CATEGORIES, blank=True
    )
    # TODO: create list of clubs?
    team = models.CharField(max_length=4, blank=True, default="IND")

    # lifts fields
    snatch_first = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    snatch_first_weight = models.IntegerField(blank=True, default=0)
    snatch_second = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    snatch_second_weight = models.IntegerField(blank=True, default=0)
    snatch_third = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    snatch_third_weight = models.IntegerField(blank=True, default=0)
    cnj_first = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    cnj_first_weight = models.IntegerField(blank=True, default=0)
    cnj_second = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    cnj_second_weight = models.IntegerField(blank=True, default=0)
    cnj_third = models.CharField(
        max_length=6, choices=LIFT_STATUS, blank=True, default=DEFAULT_LIFT_STATUS
    )
    cnj_third_weight = models.IntegerField(blank=True, default=0)

    # custom fields
    @property
    def snatches(self) -> dict[str, dict[str, str | int]]:
        """Snatches custom field

        e.g. key is attempt, then another key pair to determine if lift is made and what the weight was lifted

        Returns:
            dict[str, dict[str, str]]: snatch lifts
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
        """Clean and Jerk custom field

        e.g. key is attempt, then another key pair to determine if lift is made and what the weight was lifted

        Returns:
            dict[str, dict[str, str]]: clean and jerk lifts
        """
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

        This will return the lift attempt and the best lift e.g. ("1st", 100)

        If no attempt was made then an empty string and 0 will be returned  e.g ("", 0)

        Returns:
            tuple[str, int]: e.g. ("1st", 100) and ("", 0)
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

        This will return the lift attempt and the best lift e.g. ("1st", 100)

        If no attempt was made then an empty string and 0 will be returned  e.g ("", 0)

        Returns:
            tuple[str, int]: e.g. ("1st", 100) and ("", 0)
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
    def total_lifted(self) -> int:
        """Returns the calculated total

        This takes the best snatch and the best clean and jerk to work out the total. If one lift if not completed, then 0 will be returned.

        Returns:
            int: total e.g 200, 0
        """
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

    @cached_property
    def placing(self) -> str:
        """Returns the placing of the athlete

        e.g. 1st, 11th and '-' if no total (i.e. 0) is made

        Returns:
            str: placing (e.g. '1st', '11th' '-')
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

        def sort_lift_key(lift: dict[str, str | int]) -> tuple[int, int, int, int]:
            """This gives the keys for sorting

            Args:
                lift (dict[str, str | int]): this contains the lift data

            Returns:
                tuple[int, int, int, int]: the keys to be used in the sorted parameter
            """
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

    def clean(self, *args, **kwargs):
        """Customised validation
        1. Check if an athlete is already in a competition (if new addition, not new instance)
        2. Check if lottery_number's are used more than once per session, this cannot be entered as a unique=True since lifts are shared in different sessions/competitions (only if new instance, not update)
        3. if a lift is made, then the next lift has to be an increment
        """
        # need to check if athlete is newly created or an update
        # this validation does not need to run if it is an update
        if Lift.objects.filter(reference_id=self.reference_id).exists() == False:
            # 1. check athlete not duplicated in a competition
            sessions = Session.objects.filter(competition=self.session.competition)
            for session in sessions:
                if Lift.objects.filter(
                    session=session.reference_id, athlete=self.athlete
                ).exists():
                    raise ValidationError(_(f"{self.athlete} already in competition."))

            # 2. check lottery_number
            if Lift.objects.filter(
                session=self.session,
                lottery_number=self.lottery_number,
            ).exists():
                raise ValidationError(
                    _(f"{self.lottery_number} already exists in this session.")
                )

        DICT_PLACING = {1: "1st", 2: "2nd", 3: "3rd"}
        snatches = self.snatches
        lst_snatches = [snatch for snatch in snatches.values()]

        for i, snatch in enumerate(lst_snatches):
            if i > 0:
                if snatch["lift_status"] == "LIFT":
                    # if lift is made
                    # current weight must be greater than previous
                    if not snatch["weight"] > lst_snatches[i - 1]["weight"]:
                        raise ValidationError(
                            _(
                                f"{DICT_PLACING[i+1]} snatch cannot be lower or same than previous lift if a good lift."
                            )
                        )
                else:
                    # if lift is not made or not attempted
                    # current weight must be same or greater than previous
                    if not snatch["weight"] >= lst_snatches[i - 1]["weight"]:
                        raise ValidationError(
                            _(
                                f"{DICT_PLACING[i+1]} snatch cannot be less than previous lift."
                            )
                        )

        cnjs = self.cnjs
        lst_cnjs = [cnj for cnj in cnjs.values()]

        for i, cnj in enumerate(lst_cnjs):
            if i > 0:
                if cnj["lift_status"] == "LIFT":
                    if not cnj["weight"] > lst_cnjs[i - 1]["weight"]:
                        raise ValidationError(
                            _(
                                f"{DICT_PLACING[i+1]} clean and jerk cannot be lower or same than previous lift if a good lift."
                            )
                        )
                else:
                    if not cnj["weight"] >= lst_cnjs[i - 1]["weight"]:
                        raise ValidationError(
                            _(
                                f"{DICT_PLACING[i+1]} clean and jerk cannot be less than previous lift."
                            )
                        )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.athlete} - {self.session.competition} {self.session.competition.date_start.year}"
