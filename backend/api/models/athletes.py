from datetime import datetime

from config.settings.base import HASHID_FIELD_SALT
from django.db import models
from hashid_field import HashidAutoField


class Athlete(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    yearborn = models.IntegerField(default=1900)

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self):
        return f"{self.last_name.upper()}, {self.first_name.title()}"

    @property
    def years_from_birth(self) -> int:
        """calculatute years from birth"""
        return datetime.now().year - self.yearborn

    @property
    def is_youth(self) -> bool:
        """13-17 years"""
        return self.years_from_birth >= 13 and self.years_from_birth <= 17

    @property
    def is_junior(self) -> bool:
        """15-20 years"""
        return self.years_from_birth >= 15 and self.years_from_birth <= 20

    @property
    def is_senior(self) -> bool:
        """15+ years"""
        return self.years_from_birth > 15

    @property
    def is_master(self) -> bool:
        """35+ years"""
        return self.years_from_birth > 35

    def __str__(self):
        return self.full_name
