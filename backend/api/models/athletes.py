"""Athlete model.

This is all the Athlete model.
"""

from datetime import datetime

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField
from simple_history.models import HistoricalRecords

from config.settings import HASHID_FIELD_SALT, MINIMUM_YEAR_FROM_BIRTH

from .managers import AthleteManager
from .utils import age_category
from .utils.types import AgeCategories


def validate_yearborn(yearborn: int, validate=True):
    """Validate `yearborn` field.

    Args:
        yearborn (int): Year of athlete's birth.
        validate (boolean): If validation fails, a validation error is \
                raised. Defaults to True.

    Returns:
        Raises ValidationError or returns the ValidationError.
    """
    years_from_birth = datetime.now().year - yearborn
    validator = ValidationError(
        _("Years after %(year)s not accepted"),
        code="invalid year",
        params={"year": datetime.now().year - MINIMUM_YEAR_FROM_BIRTH},
    )
    if years_from_birth < MINIMUM_YEAR_FROM_BIRTH:
        if validate:
            raise validator
        return validator


class Athlete(models.Model):
    """Athlete model.

    Representation of the weightlifting athlete.
    """

    reference_id = HashidAutoField(
        primary_key=True, salt=f"athletemodel_reference_id_{HASHID_FIELD_SALT}"
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    yearborn = models.IntegerField(
        default=1900,
        validators=[validate_yearborn],
    )

    history = AuditlogHistoryField(pk_indexable=False)
    history_record = HistoricalRecords(
        history_id_field=HashidAutoField(
            salt=f"athlete_history_id_{HASHID_FIELD_SALT}"
        )
    )

    objects = AthleteManager()

    class Meta:
        """Athlete model settings."""

        ordering = ["last_name", "first_name"]

    @property
    def full_name(self) -> str:
        """Give full name.

        Full name is titlized `first_name` and `last_name`.

        Format: first_name + last_name
        """
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def age_categories(self) -> AgeCategories:
        """Age category of the athlete at the time of the lift."""
        return age_category(yearborn=self.yearborn)

    def __str__(self) -> str:
        """Represent athlete model as a string."""
        return self.full_name

    def clean(self, *args, **kwargs):
        """Customise validation."""
        # errors = []
        # # Yearborn validation
        # yearborn_validation = validate_yearborn(
        #     yearborn=self.yearborn, validate=True
        # )
        # if yearborn_validation:
        #     errors.append(yearborn_validation)
        #
        # if len(errors) > 0:
        #     raise ValidationError(errors)

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Necessary to enact custom validation in `clean()` method."""
        self.full_clean()
        super().save(*args, **kwargs)


auditlog.register(Athlete)
