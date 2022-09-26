"""Weight Categories"""

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from api.models.support.base_era import BaseEra
from config.settings import HASHID_FIELD_SALT

__M = "M"
__W = "W"

SEX_CHOICES = [(__M, "Men's"), (__W, "Women's")]


class WeightCategoryEra(BaseEra):
    """Era for Weight categories.

    `age_categories` is what applies to this weight categories (e.g. Youth only)
    """

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"wceramodel_reference_id_{HASHID_FIELD_SALT}",
    )
    history = AuditlogHistoryField(pk_indexable=False)


class WeightCategory(models.Model):
    """Weight category."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"weightcategoriesmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    era = models.ForeignKey(
        WeightCategoryEra, blank=True, null=True, on_delete=models.SET_NULL
    )
    age_categories = models.ManyToManyField("api.AgeCategory", blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    weight = models.IntegerField(blank=True)
    is_plus = models.BooleanField(blank=True, default=False)

    history = AuditlogHistoryField(pk_indexable=False)

    class Meta:
        """Model settings."""

        verbose_name_plural = "Weight categories"

        constraints = [
            models.UniqueConstraint(
                fields=["era", "sex", "weight"],
                name="era_sex_weight_unique_combination",
            ),
        ]

    def clean(self, *args, **kwargs):
        """Validate for weight categories.

        1. Weight must be positive.
        2. TODO: Age Category era and Weight Category era must intersect.
        """
        errors = []
        if self.weight < 0:
            errors.append(
                ValidationError(_("weight must be positive."), code="positive")
            )

        if len(errors) > 0:
            raise ValidationError(errors)

        super().clean(*args, **kwargs)

    @property
    def name(self) -> str:
        """Name of the weight class.

        Example:
            >>> WC.name
            'M69'
        """
        return f"{self.sex}{self.weight}{'+' if self.is_plus else ''}"

    def __str__(self) -> str:
        """Give string representation."""
        return self.name


auditlog.register(WeightCategory)
auditlog.register(WeightCategoryEra)
