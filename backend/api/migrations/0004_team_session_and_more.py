# Generated by Django 4.0.6 on 2022-07-22 01:52

import django.db.models.deletion
import hashid_field.field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_competition_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("team", models.CharField(blank=True, max_length=20)),
                ("location", models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Session",
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
                ("number", models.IntegerField(blank=True)),
                ("date_time", models.DateTimeField(blank=True)),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.competition",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="session",
            constraint=models.UniqueConstraint(
                fields=("competition", "number"),
                name="competition_number_unique_combination",
            ),
        ),
    ]
