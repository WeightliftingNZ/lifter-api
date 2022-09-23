"""The BaseEra abstract model.

This is used to determine when the validation of another model should be \
        enacted (e.g. grading, weight categories).
"""
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


class BaseEra(models.Model):
    """Base Era model.

    Note that this the abstracted model.

    The Era model contains one important field, `date_start`. The latest era \
            is deemed the current era. And the `date_start` of one era can be \
            used to determine the end of a previous.
    """

    # reference_id must be set on children era classes
    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"baseeramodel_reference_id_{HASHID_FIELD_SALT}",
    )
    date_start = models.DateField(blank=True, unique=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    @cached_property
    def is_current(self) -> bool:
        """Return if the era is current.

        Returns:
            (bool): True if the era is current.
        """
        return (
            self.__class__.objects.latest("date_start").reference_id
            == self.reference_id
        )

    @cached_property
    def date_end(self) -> datetime | None:
        """Provide date end for an era.

        This is determined by the `date_start` of the more recent era. If the \
                current era is the most recent, then `None` is returned.

        Returns:
            (datetime|None): The end date of the era or `None` if current.
        """
        if self.is_current:
            return None
        eras = [
            era.reference_id
            for era in list(
                self.__class__.objects.all().order_by("date_start")
            )
        ]
        current_era_idx = eras.index(self.reference_id)  # idx on the era list
        next_era_idx = eras[current_era_idx + 1]
        return (
            self.__class__.objects.filter(reference_id=next_era_idx)
            .get()
            .date_start
        )

    class Meta:
        """Settings to model."""

        abstract = True
        ordering = ["date_start"]
        app_label = "api"
        get_latest_by = ["date_start"]

    def __str__(self) -> str:
        """Give string representation."""
        if self.is_current:
            return f"{self.__class__._meta.verbose_name.title()}: {self.date_start.year} - Current"
        else:
            return f"{self.__class__._meta.verbose_name.title()}: {self.date_start.year} - {self.date_end.year}"
