from django.db import models

from hashid_field import HashidAutoField

from config.settings.base import HASHID_FIELD_SALT


class Competition(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )

    competition_name = models.CharField(max_length=128, blank=True)
    # TODO: list of gyms?
    location = models.CharField(max_length=128, blank=True)
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)

    def __str__(self):
        return f"{self.competition_name}"
