"""Set mock data and set up fixtures to be used for testing."""

from dataclasses import dataclass, field
from datetime import datetime

import pytest
from faker import Faker

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift

Faker.seed(42)
_faker = Faker("en_NZ")


@dataclass(frozen=True)
class AthleteMocker:
    """Athlete mock."""

    first_name: str = field(default_factory=_faker.first_name)
    last_name: str = field(default_factory=_faker.last_name)
    yearborn: int = field(
        default_factory=lambda: _faker.date_of_birth(minimum_age=13).year
    )


@dataclass(frozen=True)
class CompetitionMocker:
    """Competition mock."""

    date_start: datetime = field(default_factory=datetime.now)
    date_end: datetime = field(default_factory=datetime.now)
    name: str = field(
        default_factory=lambda: " ".join(["Competition", _faker.color_name])
    )
    location: str = field(default_factory=_faker.address)


@pytest.fixture(scope="session", autouse=True)
def faker():
    """Faker instance."""
    return Faker()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    """Set up local for faker."""
    return ["en_NZ"]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    """Random seed to ensure faker information is consistent."""
    return 42


@pytest.fixture(scope="session")
def mock_athlete(django_db_blocker) -> list[Athlete]:
    """Provide edited athlete data.

    Returns:
        list[Athlete]: list of mocked Athlete models.
    """
    ATHLETES = 4
    athletes = [AthleteMocker() for _ in range(ATHLETES)]
    created = []
    for athlete in athletes:
        with django_db_blocker.unblock():
            created.append(Athlete.objects.create(**athlete.__dict__))
    return created


@pytest.fixture
def mock_competition(django_db_blocker, faker) -> list[Competition]:
    """Mock competition data.

    Returns:
        list[Competition]: list of mock competitions
    """
    # COMPETITIONS = 2
    MOCK_COMPETIION_ONE = {
        "date_start": str(datetime.now())[:10],
        "date_end": str(datetime.now())[:10],
        "name": f"Competition {faker.color_name()}",
        "location": faker.company(),
    }

    MOCK_COMPETIION_TWO = {
        "date_start": faker.date_between(
            start_date=datetime(2019, 1, 1), end_date=datetime(2019, 1, 3)
        ),
        "date_end": faker.date_between(
            start_date=datetime(2019, 1, 4), end_date=datetime(2019, 1, 8)
        ),
        "name": f"Competition {faker.color_name()}",
        "location": MOCK_COMPETIION_ONE["location"],
    }
    competitions = [MOCK_COMPETIION_ONE, MOCK_COMPETIION_TWO]
    created = []
    for competition in competitions:
        with django_db_blocker.unblock():
            created.append(Competition.objects.create(**competition))
    return created


@pytest.fixture
def mock_lift(django_db_blocker, mock_competition, mock_athlete) -> list[Lift]:
    """Mock lift data.

    Returns:
        list[Lift]: list of mock lifts
    """
    lifts = [
        {  # 0
            "competition": Competition.objects.get(
                reference_id=mock_competition[0].reference_id
            ),
            "athlete": Athlete.objects.get(
                reference_id=mock_athlete[0].reference_id
            ),
            "snatch_first": "LIFT",
            "snatch_first_weight": 100,
            "snatch_second": "LIFT",
            "snatch_second_weight": 101,
            "snatch_third": "LIFT",
            "snatch_third_weight": 102,
            "cnj_first": "LIFT",
            "cnj_first_weight": 100,
            "cnj_second": "LIFT",
            "cnj_second_weight": 101,
            "cnj_third": "LIFT",
            "cnj_third_weight": 102,
            "bodyweight": 102.00,
            "weight_category": "M102+",
            "team": "TEST",
            "session_number": 0,
            "lottery_number": 1,
        },
        {  # 1
            "competition": Competition.objects.get(
                reference_id=mock_competition[0].reference_id
            ),
            "athlete": Athlete.objects.get(
                reference_id=mock_athlete[1].reference_id
            ),
            "snatch_first": "LIFT",
            "snatch_first_weight": 100,
            "snatch_second": "LIFT",
            "snatch_second_weight": 101,
            "snatch_third": "LIFT",
            "snatch_third_weight": 102,
            "cnj_first": "LIFT",
            "cnj_first_weight": 100,
            "cnj_second": "LIFT",
            "cnj_second_weight": 101,
            "cnj_third": "LIFT",
            "cnj_third_weight": 102,
            "bodyweight": 102.00,
            "weight_category": "M102+",
            "team": "TEST",
            "session_number": 0,
            "lottery_number": 2,
        },
        {  # 2
            "competition": Competition.objects.get(
                reference_id=mock_competition[1].reference_id
            ),
            "athlete": Athlete.objects.get(
                reference_id=mock_athlete[0].reference_id
            ),
            "snatch_first": "LIFT",
            "snatch_first_weight": 100,
            "snatch_second": "LIFT",
            "snatch_second_weight": 101,
            "snatch_third": "LIFT",
            "snatch_third_weight": 102,
            "cnj_first": "LIFT",
            "cnj_first_weight": 100,
            "cnj_second": "LIFT",
            "cnj_second_weight": 101,
            "cnj_third": "LIFT",
            "cnj_third_weight": 102,
            "bodyweight": 102.00,
            "weight_category": "M102+",
            "team": "TEST",
            "session_number": 0,
            "lottery_number": 1,
        },
    ]
    created = []
    for lift in lifts:
        with django_db_blocker.unblock():
            created.append(Lift.objects.create(**lift))
    return created
