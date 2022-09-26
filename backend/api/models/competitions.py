"""Competition Models."""

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

from .managers import CompetitionManager


class Competition(models.Model):
    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"competitionmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    name = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    # TODO more fields
    # city = models.CharField(max_length=128, blank=True)
    # organiser = models.CharField(
    #     max_length=128,
    #     blank=True,
    # )
    date_start = models.DateField(blank=True)
    date_end = models.DateField(blank=True)
    # TODO
    # classify status of the competition e.g club, record breaking

    history = AuditlogHistoryField(pk_indexable=False)

    objects = CompetitionManager()

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
                "%(date_start)s is invalid. Start date must be before the end date, %(date_end)s.",
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


auditlog.register(Competition)
