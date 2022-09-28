"""Competition Factories."""

import random
from datetime import datetime, timedelta

import factory
from faker import Faker

from api.models import Competition

Faker.seed(42)
fake = Faker("en_NZ")


class CompetitionFactory(factory.django.DjangoModelFactory):
    """Competition factory."""

    class Meta:
        """CompetitionFactory settings."""

        model = Competition

    name = factory.LazyFunction(lambda: f"Competition {fake.color_name()}")
    location = factory.Faker("address")
    date_start = factory.Faker("datetime")

    @factory.lazy_attribute
    def date_end(self):
        """`date_end attribute."""
        return self.date_start + timedelta(
            days=random.choice([0] * 8 + [1] * 1 + [2] * 1)
        )


class Post2019Pre2022CompetitionFactory(CompetitionFactory):
    """Competition factory for competitions between 2019 and 2022."""

    date_start = factory.Faker(
        "date_between_dates",
        date_start=datetime(2019, 1, 1),
        date_end=datetime(2022, 1, 1),
    )
