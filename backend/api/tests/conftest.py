"""Set mock data and set up fixtures to be used for testing."""

import logging
import random
from datetime import datetime

import factory.random
import faker.config
import pytest
from django.db import connection
from pytest_factoryboy import register

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift
from config.settings import PAGE_SIZE

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
def athlete_with_lifts():
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
def mock_competition() -> list[Competition]:
    """Mock competition data.

    Returns:
        list[Competition]: list of mock competitions
    """
    # COMPETITIONS = 2
    MOCK_COMPETIION_ONE = Post2019Pre2022CompetitionFactory()
    MOCK_COMPETIION_TWO = Post2019Pre2022CompetitionFactory(
        location=MOCK_COMPETIION_ONE.location
    )
    return [MOCK_COMPETIION_ONE, MOCK_COMPETIION_TWO]


@pytest.fixture
def mock_lift(mock_competition, mock_athlete) -> list[Lift]:
    """Mock lift data.

    Returns:
        list[Lift]: list of mock lifts
    """
    return [
        LiftFactory(
            competition=mock_competition[0],
            athlete=mock_athlete[0],
            session_number=0,
            lottery_number=1,
        ),
        LiftFactory(
            competition=mock_competition[0],
            athlete=mock_athlete[1],
            session_number=0,
            lottery_number=2,
        ),
        LiftFactory(
            competition=mock_competition[1],
            athlete=mock_athlete[0],
            session_number=0,
            lottery_number=1,
        ),
    ]
