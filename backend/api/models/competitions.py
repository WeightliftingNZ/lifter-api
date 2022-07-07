"""Competition Models."""

from django.db import models
from hashid_field import HashidAutoField

from config.settings.base import HASHID_FIELD_SALT


class Competition(models.Model):
    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"competitionmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    competition_name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)

    class Meta:
        ordering = ["-date_start", "competition_name"]

    def __str__(self):
        return f"{self.competition_name} {self.date_start.year}"
