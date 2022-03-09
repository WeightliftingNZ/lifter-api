from django.db import models

from .utils import WEIGHT_CATEGORIES, LIFT_STATUS
from . import Athlete, Competition


class Lift(models.Model):
    lift_id = models.AutoField(primary_key=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

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
    session_number = models.IntegerField(blank=True)
    session_datetime = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.athlete} - {self.competition} {self.competition.date_start.year}"
