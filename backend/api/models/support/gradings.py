"""Grading Models.

This contains the grading for all for lifts.

Grades are usually released as a group.
"""

# from django.core.exceptions import ValidationError
# from django.db import models
# from hashid_field import HashidAutoField
#
# from config.settings import HASHID_FIELD_SALT


# class Grade(models.Model):
#     """Grades for a weight category."""
#
#     reference_id = HashidAutoField(
#         primary_key=True,
#         salt=f"gradesmodel_reference_id_{HASHID_FIELD_SALT}",
#     )
#     era = models.ForeignKey("api.GradeEra", on_delete=models.CASCADE)
#     weight_category = models.ForeignKey(
#         "api.WeightCategory", on_delete=models.CASCADE
#     )
#     age_category = models.ForeignKey(
#         "api.AgeCategory", on_delete=models.CASCADE
#     )
#
#     class Meta:
#         """Model settings."""
#
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["era", "weight_category", "age_category"],
#                 name="era_age_weight_unique_combination",
#             ),
#         ]
#
#
# class GradeType(models.Model):
#     """Grade types.
#
#     e.g.
#     name = "Grade A"
#     minimum_weight = 200
#     """
#
#     reference_id = HashidAutoField(
#         primary_key=True,
#         salt=f"gradetypemodel_reference_id_{HASHID_FIELD_SALT}",
#     )
#     name = models.CharField(max_length=32, blank=True)
#     grade = models.ForeignKey("api.Grade", on_delete=models.CASCADE)
#     minimum_weight = models.IntegerField(blank=True)
#
#     class Meta:
#         """Model settings."""
#
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["name", "grade", "minimum_weight"],
#                 name="era_age_minumum_weight_combination",
#             ),
#         ]
