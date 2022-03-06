from django.db import models

from hashid_field import HashidAutoField

from config.settings.base import HASHID_FIELD_SALT, DEFAULT_AUTO_FIELD
from api.choices import WEIGHT_CATEGORIES, LIFT_STATUS


class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = "api"


class AthleteModel(BaseModel):
    # pre-populated
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    yearborn = models.IntegerField(default=1900)

    def __str__(self):
        return f"{self.last_name.upper()}, {self.first_name.title()}"


class CompetitionModel(BaseModel):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    date_start = models.DateTimeField(blank=True)
    date_end = models.DateTimeField(blank=True)
    location = models.CharField(max_length=128, blank=True)
    competition_name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.competition_name}"


class SessionModel(BaseModel):
    session_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(CompetitionModel, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.competition} - {self.session_id}"


class LifterModel(BaseModel):
    lifter_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(CompetitionModel, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE)
    athlete = models.ForeignKey(AthleteModel, on_delete=models.CASCADE)

    snatch_first = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    snatch_first_weight = models.IntegerField(blank=True)
    snatch_second = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    snatch_second_weight = models.IntegerField(blank=True)
    snatch_third = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    snatch_third_weight = models.IntegerField(blank=True)
    cnj_first = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
    cnj_first_weight = models.IntegerField(blank=True)
    cnj_second = models.CharField(max_length=6, choices=LIFT_STATUS, blank=True)
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

    def __str__(self):
        return f"{self.athlete}"
