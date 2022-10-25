"""Set mock data and set up fixtures to be used for testing."""

import logging
import random
from datetime import datetime

import factory.random
import faker.config
import pytest
from django.db import connection
from faker import Faker
from pytest_factoryboy import register

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift
from config.settings import MINIMUM_YEAR_FROM_BIRTH, PAGE_SIZE

from .factories import (
    AthleteFactory,
    CompetitionFactory,
    CurrentYearCompetitionFactory,
    JuniorAthleteFactory,
    LiftFactory,
    MastersAthleteFactory,
    Post1992Pre2017CompetitionFactory,
    Post2017Pre2018CompetitionFactory,
    Post2019Pre2022CompetitionFactory,
    SeniorAthleteFactory,
    YouthAthleteFactory,
)

register(AthleteFactory)
register(YouthAthleteFactory)
register(JuniorAthleteFactory)
register(SeniorAthleteFactory)
register(MastersAthleteFactory)
register(CompetitionFactory)
register(CurrentYearCompetitionFactory)
register(Post2019Pre2022CompetitionFactory)
register(Post1992Pre2017CompetitionFactory)
register(Post2017Pre2018CompetitionFactory)
register(LiftFactory)


TEST_RANDOM_SEED = 42

faker.config.DEFAULT_LOCALE = "en_NZ"
factory.random.reseed_random(TEST_RANDOM_SEED)
random.seed(TEST_RANDOM_SEED)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Test database setup.

    Installing `pg_trgm` on to the test database, other wise '%' will not be \
            recognised.
    """
    logging.info(django_db_setup)
    with django_db_blocker.unblock(), connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


@pytest.fixture
def batch_athlete() -> list[Athlete]:
    """Create athletes at random, the number one more than the page size."""
    return AthleteFactory.create_batch(PAGE_SIZE + 1)


@pytest.fixture
def athlete_with_lifts() -> Athlete:
    """Create an athlete."""
    athlete = AthleteFactory(yearborn=datetime.now().year - 45)
    competitions = (
        CurrentYearCompetitionFactory.create_batch(4)
        + Post2019Pre2022CompetitionFactory.create_batch(4)
        + Post2017Pre2018CompetitionFactory.create_batch(4)
        + Post1992Pre2017CompetitionFactory.create_batch(8)
    )
    for competition in competitions:
        LiftFactory(
            athlete=athlete,
            competition=competition,
        )
    return athlete


@pytest.fixture
def athlete_with_no_total() -> Athlete:
    """Create an athlete with one lift and no total."""
    lift = LiftFactory(
        snatch_first="DNA", snatch_second="DNA", snatch_third="DNA"
    )
    return lift.athlete


@pytest.fixture
def batch_competition() -> list[Competition]:
    """Create competitions at random, the number one more than the page size."""
    return CompetitionFactory.create_batch(PAGE_SIZE + 1)


@pytest.fixture
def competition_with_lifts() -> Competition:
    """Create a competition with lifts."""
    # Faker is defined here because it is thread unsafe
    Faker.seed(42)
    fake = Faker("en_NZ")
    competition = CompetitionFactory()
    for _ in range(20):
        # ensure athlete is old enough to compete
        athlete = AthleteFactory(
            yearborn=fake.date_between(
                end_date=datetime(
                    competition.date_start.year - MINIMUM_YEAR_FROM_BIRTH + 1,
                    1,
                    1,
                ),
            ).year
        )
        LiftFactory(athlete=athlete, competition=competition)
    return competition


@pytest.fixture
def batch_lift() -> list[Lift]:
    """Create a batch of lifts."""
    return LiftFactory.create_batch(10)


@pytest.fixture
def competition_with_lifts_weight_categories() -> tuple[Competition, list]:
    """Create lifts with given weight_categories."""
    competition = Post2019Pre2022CompetitionFactory()
    weight_categories_original = [
        wc
        for wc in ["W45", "W87", "W87+", "M55", "M109", "M109+"]
        for _ in range(random.randint(1, 10))
    ]
    weight_categories = weight_categories_original[:]
    random.shuffle(weight_categories)
    for weight_category in weight_categories:
        LiftFactory(competition=competition, weight_category=weight_category)
    return competition, weight_categories_original
