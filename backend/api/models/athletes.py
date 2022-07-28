"""Athlete model.

This is all the Athlete model.
"""

from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

from .utils import age_category
from .utils.types import AgeCategories

MINIMUM_YEAR_FROM_BIRTH = 5


def check_yearborn(yearborn: Any) -> None:
    """Check is the start date is before the end date."""
    # TODO: What is the youngest someone can lift?
    years_from_birth = datetime.now().year - yearborn
    if years_from_birth < MINIMUM_YEAR_FROM_BIRTH:
        raise ValidationError(
            _("Years after %(year)s not accepted."),
            code="invalid year",
            params={"year": datetime.now().year - MINIMUM_YEAR_FROM_BIRTH},
        )


class Athlete(models.Model):
    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    yearborn = models.IntegerField(default=1900, validators=[check_yearborn])

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def full_name(self) -> str:
        """Give full name.

        Format: LASTNAME, firstname.
        """
        return f"{self.last_name.upper()}, {self.first_name.title()}"

    @property
    def age_categories(self) -> AgeCategories:
        """Age category of the athlete at the time of the lift."""
        return age_category(yearborn=self.yearborn)

    def __str__(self) -> str:
        return self.full_name
