"""Competition Factories."""

import random
from datetime import datetime, timedelta

import factory

from api.models import Competition

from .fake import fake


class CompetitionFactory(factory.django.DjangoModelFactory):
    """Competition factory."""

    class Meta:
        """CompetitionFactory settings."""

        model = Competition

    name = factory.LazyFunction(lambda: f"Competition {fake.color_name()}")
    location = factory.Faker("address")
    date_start = factory.Faker("date")

    @factory.lazy_attribute
    def date_end(self):
        """`date_end attribute."""
        date_start = self.date_start
        if isinstance(date_start, str):
            date_start = datetime.strptime(self.date_start, "%Y-%m-%d")
        return date_start + timedelta(
            days=random.choice([0] * 8 + [1] * 1 + [2] * 1)
        )


class CurrentYearCompetitionFactory(CompetitionFactory):
    """Competition factory for competition in the current year."""

    _now = datetime.now()

    date_start = factory.Faker(
        "date_between_dates",
        date_start=datetime(_now.year, 1, 1),
        date_end=datetime(_now.year, _now.month, _now.day),
    )


class Post2019Pre2022CompetitionFactory(CompetitionFactory):
    """Competition factory for competitions between 2019 and 2022."""

    date_start = factory.Faker(
        "date_between_dates",
        date_start=datetime(2019, 1, 1),
        date_end=datetime(2022, 1, 1),
    )


class Post2017Pre2018CompetitionFactory(CompetitionFactory):
    """Competition factory for competitions between 2017 and 2018."""

    date_start = factory.Faker(
        "date_between_dates",
        date_start=datetime(2017, 1, 1),
        date_end=datetime(2018, 1, 1),
    )


class Post1992Pre2017CompetitionFactory(CompetitionFactory):
    """Competition factory for competitions between 1992 and 2017."""

    date_start = factory.Faker(
        "date_between_dates",
        date_start=datetime(1992, 1, 1),
        date_end=datetime(2017, 1, 1),
    )
