"""Grading Models.

This contains the grading for all for lifts.

Grades are usually released as a group.
"""
# TODO: Look into this for the future

from django.core.exceptions import ValidationError
from django.db import models
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT

__M = "M"
__W = "W"

SEX_CHOICES = [(__M, "Men's"), (__W, "Women's")]


class BaseModelEra(models.Model):
    """Base model methods.

    A `date_end` set to null indicates that this is the current era.
    """

    date_start = models.DateField(blank=True, unique=True)
    date_end = models.DateField(null=True, blank=True, unique=True)

    class Meta:
        """Settings to model."""

        abstract = True
        ordering = ["-date_start"]

    def clean(self, *args, **kwargs):
        """Customise validation.

        1. `date_start` must be before `date_end`.
        2. TODO: Ensure there is no overlap in eras.
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

        # TODO: ensure there is no overlap in eras
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Enact custom validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Give string representation."""
        if self.date_end is None:
            return f"{self.date_start.year} - Current"
        else:
            return f"{self.date_start.year} - {self.date_end.year} "


class AgeCategoryEra(BaseModelEra):
    """Provide date ranges for age categories of a certain era.

    Examples:
        >>> str(AgeCategoryEra.objects.first())
        '2018 - Current'
    """

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"agecategoryeramodel_reference_id_{HASHID_FIELD_SALT}",
    )


class AgeCategory(models.Model):
    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"agecategorymodel_reference_id_{HASHID_FIELD_SALT}",
    )
    age_category_era = models.ForeignKey(
        "api.AgeCategoryEra", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=32, blank=True)
    upper_age_bound = models.IntegerField(null=True, blank=True)
    lower_age_bound = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "age_categories"


class WeightCategoryEra(BaseModelEra):
    """Provide date range for weight categories of a certain era."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"weightcategoryeramodel_reference_id_{HASHID_FIELD_SALT}",
    )


class WeightCategory(models.Model):
    """Weight category.

    Examples:
        >>> str(WeightCategory.objects.first())
        'M69'
    """

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"weightcategoriesmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    era = models.ForeignKey("api.WeightCategoryEra", on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    weight = models.IntegerField(blank=True)

    class Meta:
        """Model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=["era", "sex", "weight"],
                name="era_sex_weight_unique_combination",
            ),
        ]

    def __str__(self) -> str:
        """Give string representation."""
        return f"{self.sex}{self.weight}"


class GradeEra(BaseModelEra):
    """Binds grade to a certain date."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"gradingeramodel_reference_id_{HASHID_FIELD_SALT}",
    )


class Grade(models.Model):
    """Grades for a weight category."""

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"gradesmodel_reference_id_{HASHID_FIELD_SALT}",
    )
    era = models.ForeignKey("api.GradeEra", on_delete=models.CASCADE)
    weight_category = models.ForeignKey(
        "api.WeightCategory", on_delete=models.CASCADE
    )
    age_category = models.ForeignKey(
        "api.AgeCategory", on_delete=models.CASCADE
    )

    class Meta:
        """Model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=["era", "weight_category", "age_category"],
                name="era_age_weight_unique_combination",
            ),
        ]


class GradeType(models.Model):
    """Grade types.

    e.g.
    name = "Grade A"
    minimum_weight = 200
    """

    reference_id = HashidAutoField(
        primary_key=True,
        salt=f"gradetypemodel_reference_id_{HASHID_FIELD_SALT}",
    )
    name = models.CharField(max_length=32, blank=True)
    grade = models.ForeignKey("api.Grade", on_delete=models.CASCADE)
    minimum_weight = models.IntegerField(blank=True)

    class Meta:
        """Model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "grade", "minimum_weight"],
                name="era_age_minumum_weight_combination",
            ),
        ]
