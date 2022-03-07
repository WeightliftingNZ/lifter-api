from django.db import models

from hashid_field import HashidAutoField

from config.settings.base import HASHID_FIELD_SALT


class Athlete(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athlete_reference_id_{HASHID_FIELD_SALT}"
    )

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    yearborn = models.IntegerField(default=1900)

    def __str__(self):
        return f"{self.last_name.upper()}, {self.first_name.title()}"
