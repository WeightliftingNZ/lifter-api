# Self generated

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "api",
            "0006_remove_lift_session_lottery_unique_combination_and_more",
        )
    ]

    operations = [TrigramExtension()]
