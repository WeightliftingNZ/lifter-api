"""Set mock data and set up fixtures to be used for testing."""

import logging

import factory.random
import faker.config
import pytest
from django.db import connection
from pytest_factoryboy import register

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift

from .factories import (
    AthleteFactory,
    CompetitionFactory,
    JuniorAthleteFactory,
    LiftFactory,
    MastersAthleteFactory,
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
register(Post2019Pre2022CompetitionFactory)
register(LiftFactory)


faker.config.DEFAULT_LOCALE = "en_NZ"
factory.random.reseed_random(42)


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
def mock_athlete() -> list[Athlete]:
    """Provide edited athlete data.

    Returns:
        list[Athlete]: list of mocked Athlete models.
    """
    ATHLETES = 4
    return [AthleteFactory() for _ in range(ATHLETES)]


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
