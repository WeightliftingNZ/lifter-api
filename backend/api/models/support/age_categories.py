"""Age categories for lifters.

From: https://iwf.sport/weightlifting_/participants/
    - YOUTH: 13 – 17 years of age
    - JUNIOR: 15 – 20 years of age
    - SENIOR: ≥15 years of age
    - MASTERS: ≥35 years of age

Masters age categories:
    - 35-39
    - 40-44
    - 45-49
    - 50-54
    - 55-59
    - 60-64
    - 65-69
    - 70+
"""

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from api.models.support.base_era import BaseEra
from config.settings import HASHID_FIELD_SALT


class AgeCategoryEra(BaseEra):
    """Era for Age categories."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"aceramodel_reference_id_{HASHID_FIELD_SALT}",
    )
    history = AuditlogHistoryField(pk_indexable=False)


class AgeCategory(models.Model):
    """Age Category."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"agecategorymodel_reference_id_{HASHID_FIELD_SALT}",
    )
    era = models.ForeignKey(
        AgeCategoryEra,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(max_length=32, blank=True)
    upper_age_bound = models.IntegerField(null=True, blank=True)
    lower_age_bound = models.IntegerField(blank=True, default=0)

    history = AuditlogHistoryField(pk_indexable=False)

    class Meta:
        """Model settings."""

        verbose_name_plural = "Age categories"
        ordering = ["lower_age_bound", "upper_age_bound"]

    def clean(self, *args, **kwargs):
        """Validate for age bounds.

        1. Age bounds must be positive.
        2. `upper_age_bound` must be larger than the `lower_age_bound`.
        3. Check Era is set to right choice field.
        """
        errors = []
        if self.upper_age_bound is not None and self.upper_age_bound < 0:
            errors.append(
                ValidationError(
                    _("upper_age_bound must be positive."), code="positive"
                )
            )

        if self.lower_age_bound < 0:
            errors.append(
                ValidationError(
                    _("lower_age_bound must be positive."), code="positive"
                )
            )

        if (
            self.upper_age_bound is not None
            and self.upper_age_bound < self.lower_age_bound
        ):
            errors.append(
                ValidationError(
                    _("upper_age_bound must be larger than lower_age_bound"),
                    code="bounds",
                )
            )

        if len(errors) > 0:
            raise ValidationError(errors)

        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Necessary to enact custom validation in `clean()` method."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Represent string."""
        if self.upper_age_bound is None:
            return f"{self.name}: {self.lower_age_bound} <= age"
        return f"{self.name}: {self.lower_age_bound} <= age <= {self.upper_age_bound}"


auditlog.register(AgeCategoryEra)
auditlog.register(AgeCategory)
