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
    athlete_1 = {
        "first_name": "One",
        "last_name": "Athlete-One",
        "yearborn": 2001,
    }
    athlete_2 = {
        "first_name": "Two",
        "last_name": "Athlete-Two",
        "yearborn": 2002,
    }
    # TODO: don't need athlete 3 and 4 ???
    athlete_3 = {
        "first_name": "Three",
        "last_name": "Athlete-Three",
        "yearborn": 2003,
    }
    athlete_4 = {
        "first_name": "Four",
        "last_name": "Athlete-Four",
        "yearborn": 2004,
    }
    created = []
    for athlete in [athlete_1, athlete_2, athlete_3, athlete_4]:
        with django_db_blocker.unblock():
            created.append(Athlete.objects.create(**athlete))
    return created


@pytest.fixture
def mock_competition(django_db_blocker) -> dict[str, str | dict[str, str]]:
    """Mock competition data.

    Returns:
        dict[str, str | dict[str, str]]
    """
    competition_1 = {
        "date_start": "2022-01-01",
        "date_end": "2022-01-01",
        "location": "One",
        "competition_name": "Competition One",
    }
    competition_2 = {
        "date_start": "2022-02-02",
        "date_end": "2022-02-02",
        "location": "Two",
        "competition_name": "Competition Two",
    }
    created = []
    for competition in [competition_1, competition_2]:
        with django_db_blocker.unblock():
            created.append(Competition.objects.create(**competition))
    return created


@pytest.fixture
def mock_lift(
    django_db_blocker, mock_competition, mock_athlete
) -> dict[str, str | dict[str, str]]:
    """Mock lift data.

    Returns:
        dict[str, str | dict[str, str]]
    """
    lift_1 = {
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
    }
    lift_2 = {
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
    }
    lift_3 = {
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
    }
    created = []
    for lift in [lift_1, lift_2, lift_3]:
        with django_db_blocker.unblock():
            created.append(Lift.objects.create(**lift))
    return created
