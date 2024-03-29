# Generated by Django 4.1.1 on 2022-09-22 03:13

import django.db.models.deletion
import hashid_field.field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_delete_era"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgeCategory",
            fields=[
                (
                    "reference_id",
                    hashid_field.field.HashidAutoField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                        min_length=7,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=32)),
                (
                    "upper_age_bound",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "lower_age_bound",
                    models.IntegerField(blank=True, default=0),
                ),
            ],
            options={
                "verbose_name_plural": "age_categories",
                "ordering": ["lower_age_bound", "upper_age_bound"],
            },
        ),
        migrations.CreateModel(
            name="Era",
            fields=[
                (
                    "reference_id",
                    hashid_field.field.HashidAutoField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                        min_length=7,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_start", models.DateField(blank=True)),
                (
                    "category_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("WGT", "Weight Categories"),
                            ("AGE", "Age Categories"),
                            ("GRD", "Grades"),
                            ("SC", "Sinclair"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
            ],
            options={
                "ordering": ["-date_start"],
                "get_latest_by": ["-date_start"],
            },
        ),
        migrations.AddConstraint(
            model_name="era",
            constraint=models.UniqueConstraint(
                fields=("category_type", "date_start"),
                name="category_type_date_start_unique_combination",
            ),
        ),
        migrations.AddField(
            model_name="agecategory",
            name="era",
            field=models.ForeignKey(
                limit_choices_to={"category_type": "AGE"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.era",
            ),
        ),
    ]
