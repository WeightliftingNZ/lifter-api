"""Not using this anymore."""


from django.db import models
from django.utils.timezone import now
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


# TODO: Not using this model
class Team(models.Model):
    """Team model."""

    reference_id = HashidAutoField(
        primary_key=True, salt=f"teammodel_reference_id_{HASHID_FIELD_SALT}"
    )
    date_established = models.DateField(blank=True, default=now)
    date_ended = models.DateField(null=True)
    name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
