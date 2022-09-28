"""Lift factories."""

import random
from decimal import Decimal
from typing import Literal

import factory
from faker import Faker

from api.models import Lift

from .athletes import AthleteFactory
from .competitions import CompetitionFactory

Faker.seed(42)
fake = Faker("en_NZ")

LiftStatusT = Literal["LIFT", "NOLIFT", "DNA"]


def _determine_lift_status(previous_lift_status: LiftStatusT = None):
    STATUS = ("LIFT", "NOLIFT", "DNA")
    if previous_lift_status == "DNA":
        return "DNA"
    return random.choices(STATUS, (70, 25, 1), k=1)[0]


def _determine_lift(
    previous_lift: tuple[LiftStatusT, int] = None,
) -> int:
    """Randomise lift weight."""
    if previous_lift is None:
        return random.randint(15, 200)
    status, weight = previous_lift
    return {
        "DNA": 0,
        "LIFT": weight + random.randint(1, 20),
        "NOLIFT": weight + random.randint(0, 20),
    }.get(status)


class LiftFactory(factory.django.DjangoModelFactory):
    """Lift factory."""

    # TODO: will this work?

    class Meta:
        """LiftFactory settings."""

        model = Lift

    athlete = factory.SubFactory(AthleteFactory)
    competition = factory.SubFactory(CompetitionFactory)

    @factory.lazy_attribute
    def snatch_first(self):
        """First snatch category."""
        return _determine_lift_status()

    @factory.lazy_attribute
    def snatch_first_weight(self):
        """First snatch weight."""
        return _determine_lift()

    @factory.lazy_attribute
    def snatch_second(self):
        """Second snatch category."""
        return _determine_lift_status(self.snatch_first)

    @factory.lazy_attribute
    def snatch_second_weight(self):
        """Second snatch weight."""
        return _determine_lift((self.snatch_first, self.snatch_first_weight))

    @factory.lazy_attribute
    def snatch_third(self):
        """Third snatch category."""
        return _determine_lift_status(self.snatch_second)

    @factory.lazy_attribute
    def snatch_third_weight(self):
        """Third snatch weight."""
        return _determine_lift((self.snatch_second, self.snatch_second_weight))

    @factory.lazy_attribute
    def cnj_first(self):
        """First clean and jerk status."""
        return _determine_lift_status()

    @factory.lazy_attribute
    def cnj_first_weight(self):
        """First clean and jerk weight."""
        return _determine_lift()

    @factory.lazy_attribute
    def cnj_second(self):
        """Second clean and jerk status."""
        return _determine_lift_status(self.cnj_first)

    @factory.lazy_attribute
    def cnj_second_weight(self):
        """Second clean and jerk weight."""
        return _determine_lift((self.cnj_first, self.cnj_first_weight))

    @factory.lazy_attribute
    def cnj_third(self):
        """Third clean and jerk status."""
        return _determine_lift_status(self.cnj_second)

    @factory.lazy_attribute
    def cnj_third_weight(self):
        """Third clean and jerk weight."""
        return _determine_lift((self.cnj_second, self.cnj_second_weight))

    @factory.lazy_attribute
    def bodyweight(self):
        """Generate random bodyweight."""
        return round(Decimal(random.uniform(50, 150)), 2)

    # TODO: weight cats
    weight_category = "M96"
    team = factory.Faker("company")
    session_number = factory.Sequence(int)
    lottery_number = factory.Sequence(int)
