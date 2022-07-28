"""Set mock data and set up fixtures to be used for testing."""

import pytest

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift


@pytest.fixture
def mock_athlete(django_db_blocker) -> list[Athlete]:
    """Provide edited athlete data.

    Returns:
        list[Athlete]: list of mocked Athlete models.
    """
    athletes = [
        {
            "first_name": "One",
            "last_name": "Athlete-One",
            "yearborn": 2001,
        },
        {
            "first_name": "Two",
            "last_name": "Athlete-Two",
            "yearborn": 2002,
        },
    ]
    created = []
    for athlete in athletes:
        with django_db_blocker.unblock():
            created.append(Athlete.objects.create(**athlete))
    return created


@pytest.fixture
def mock_competition(django_db_blocker) -> list[Competition]:
    """Mock competition data.

    Returns:
        list[Competition]: list of mock competitions
    """
    competitions = [
        {
            "date_start": "2022-01-01",
            "date_end": "2022-01-01",
            "location": "One",
            "name": "Competition One",
        },
        {
            "date_start": "2022-02-02",
            "date_end": "2022-02-02",
            "location": "Two",
            "name": "Competition Two",
        },
    ]
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
