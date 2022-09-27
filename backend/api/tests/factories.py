"""Factories for testing. Will be applied for the future code."""

import factory
from faker import Faker

from api.models import Athlete

Faker("en_NZ")
fake = Faker().seed(42)


class AthleteFactory(factory.django.DjangoModelFactory):
    """Athlete factory."""

    class Meta:
        model = Athlete

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    yearborn = factory.Faker("date_of_birth", minimum_age=13)
