"""Competition Models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


class Competition(models.Model):
    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"competitionmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    # city = models.CharField(max_length=128, blank=True)
    # organiser = models.CharField(
    #     max_length=128,
    #     blank=True,
    # )
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)

    class Meta:
        ordering = ["-date_start", "name"]

    def __str__(self):
        return f"{self.name} {self.date_start.year}"

    def clean(self, *args, **kwargs):
        """Customise validation.

        1. `date_start` must be before `date_end`.
        """
        # 1. error if start date before end date
        if self.date_start > self.date_end:
            raise ValidationError(
                _(
                    "%(date_start)s is invalid. Start date must be before the end date, %(date_end)s."
                ),
                code="date error",
                params={
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                },
            )
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
