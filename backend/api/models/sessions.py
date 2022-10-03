"""Not yet implemented."""

from django.db import models
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


# TODO: Not using this model
class Session(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"sessionmodel_reference_id_{HASHID_FIELD_SALT}"
    )
    competition = models.ForeignKey(
        "api.Competition", on_delete=models.CASCADE
    )
    number = models.IntegerField(blank=True)
    date_time = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["competition", "number"],
                name="competition_number_unique_combination",
            ),
        ]
