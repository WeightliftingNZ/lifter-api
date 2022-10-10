"""Athete related test factories."""

import factory

from api.models import Athlete

from .fake import fake


class AthleteFactory(factory.django.DjangoModelFactory):
    """Athlete factory."""

    class Meta:
        """AthleteFactory settings."""

        model = Athlete

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    yearborn = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=13).year
    )


class YouthAthleteFactory(AthleteFactory):
    """Youth Athlete Factory."""

    yearborn = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=13, maximum_age=17).year
    )


class JuniorAthleteFactory(AthleteFactory):
    """Junior Athlete Factory."""

    yearborn = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=15, maximum_age=20).year
    )


class SeniorAthleteFactory(AthleteFactory):
    """Senior Athlete Factory."""

    yearborn = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=20).year
    )


class MastersAthleteFactory(AthleteFactory):
    """Masters Athlete Factory."""

    yearborn = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=35).year
    )
