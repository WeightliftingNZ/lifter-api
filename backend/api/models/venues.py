"""Not being implemented."""

from django.db import models
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


class Venue(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"venuemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    name = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
