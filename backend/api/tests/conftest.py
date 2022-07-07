"""Set mock data and set up fixtures to be used for testing.

Some important features:
- `competition_ids` - the keys are competitions ids, the values for this will 
be list of dictionaries, in which these dictionaries will have session ids as 
keys and lift ids as values.
- `athlete_ids` - the keys are athlete ids and the values are a list of lift 
ids.

>>> competition_ids
>>> {
    'comp_id_0': {
        [lift_id_0', 'lift_id_1'],
    },
    'comp_id_1': {
        [lift_id_4', 'lift_id_5', 'lift_id_6', 'lift_id_7'],
    }

>>> athlete_ids
>>> {
        'athlete_id_0': ['lift_id_0', 'lift_id_4'],
        'athlete_id_1': ['lift_id_1', 'lift_id_5'],
        'athlete_id_2': ['lift_id_2', 'lift_id_6'],
        'athlete_id_3': ['lift_id_3', 'lift_id_7'],
    }
"""
import pytest

from api.models.athletes import Athlete
from api.models.competitions import Competition
from api.models.lifts import Lift

from .mock_data import LIFTS


#############
# Mock Data #
#############
# @pytest.fixture
# def athletes() -> tuple[
#     dict[str, str | int],
#     dict[str, str | int],
#     dict[str, str | int],
#     dict[str, str | int],
# ]:
#     """Mock data for athlete. Can use this to access athlete data."""
#     ATHLETES = (
#         {  # a0
#             "first_name": "Athlete",
#             "last_name": "ZERO",
#             "yearborn": 2000,
#         },
#         {  # a1
#             "first_name": "Athlete",
#             "last_name": "ONE",
#             "yearborn": 2001,
#         },
#         {  # a2
#             "first_name": "Athlete",
#             "last_name": "TWO",
#             "yearborn": 2002,
#         },
#         {  # a3
#             "first_name": "Athlete",
#             "last_name": "THREE",
#             "yearborn": 2003,
#         },
#     )
#     return ATHLETES
#
# @pytest.fixture
# def create_athletes(athletes, django_db_blocker) -> dict[str, list]:
#     """Create mock athletes.
#
#     >>> athlete_ids
#     >>> {
#             'athlete_id_0': [],
#             'athlete_id_1': [],
#             'athlete_id_2': [],
#             'athlete_id_3': [],
#         }
#
#     Returns:
#         dict[str, list]: athlete id and associated lifts.
#     """
#     athlete_ids = {}
#     for athlete in athletes:
#         with django_db_blocker.unblock():
#             created = Athlete.objects.create(**athlete)
#         athlete_ids[str(created.reference_id)] = []
#     return athlete_ids
#
# @pytest.fixture
# def competitions() -> tuple[
#     dict[str, str],
#     dict[str, str],
# ]:
#     """Mock data for competitions."""
#     COMPETITIONS = (
#         {  # c0
#             "date_start": "2022-01-01",
#             "date_end": "2022-01-02",
#             "location": "Location",
#             "competition_name": "Competition Zero",
#         },
#         {  # c1
#             "date_start": "2022-02-01",
#             "date_end": "2022-02-02",
#             "location": "Location",
#             "competition_name": "Competition One",
#         },
#         )
#     return COMPETITIONS
#
# @pytest.fixture
# def create_competitions(competitions, django_db_blocker) -> dict[str, dict]:
#     """Create mock competition data.
#
#     >>> competition_ids
#     >>> {
#             'comp_id_0': {},
#             'comp_id_1': {}
#         }
#     """
#     competition_ids = {}
#     for competition in competitions:
#         with django_db_blocker.unblock():
#             created = Competition.objects.create(**competition)
#         competition_ids[str(created.reference_id)] = {}
#     return competition_ids
#
# def lifts() -> tuple[
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         dict[str, int|float|str],
#         ]:
#     """Mock data for lifts."""
#     LIFTS = (
#         {  # l0
#             "athlete": 0,
#             "competition": 0,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,
#             "lottery_number": 0,
#         },
#         {  # l1
#             "athlete": 1,
#             "competition": 0,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,
#             "lottery_number": 1,
#         },
#         {  # l2
#             "athlete": 2,
#             "competition": 0,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 1,
#             "lottery_number": 0,
#         },
#         {  # l3
#             "athlete": 3,
#             "competition": 0,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 1,
#             "lottery_number": 1,
#         },
#         {  # l4
#             "athlete": 0,
#             "competition": 1,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,  # session 0 of comp 0
#             "lottery_number": 0,
#         },
#         {  # l5
#             "athlete": 1,
#             "competition": 1,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,  # session 0 of comp 0
#             "lottery_number": 1,
#         },
#         {  # l6
#             "athlete": 2,
#             "competition": 1,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,  # session 0 of comp 0
#             "lottery_number": 2,
#         },
#         {  # l7
#             "athlete": 3,
#             "competition": 1,
#             "snatch_first": "LIFT",
#             "snatch_first_weight": 100,
#             "snatch_second": "LIFT",
#             "snatch_second_weight": 101,
#             "snatch_third": "LIFT",
#             "snatch_third_weight": 102,
#             "cnj_first": "LIFT",
#             "cnj_first_weight": 100,
#             "cnj_second": "LIFT",
#             "cnj_second_weight": 101,
#             "cnj_third": "LIFT",
#             "cnj_third_weight": 102,
#             "bodyweight": 102.00,
#             "weight_category": "M102+",
#             "team": "TEST",
#             "session_number": 0,  # session 0 of comp 0
#             "lottery_number": 3,
#         },
#     )
#     return LIFTS
#
# @pytest.fixture
# def create_lifts(create_sessions, create_athletes):
#     """Create mock lift data.
#
#     >>> competition_ids
#     >>> {
#         'comp_id_0': ['lift_id_0', 'lift_id_1', 'lift_id_2', 'lift_id_3'],
#         'comp_id_1': ['lift_id_4', 'lift_id_5', 'lift_id_6', 'lift_id_7'],
#         }
#
#     >>> athlete_ids
#     >>> {
#             'athlete_id_0': ['lift_id_0', 'lift_id_4'],
#             'athlete_id_1': ['lift_id_1', 'lift_id_5'],
#             'athlete_id_2': ['lift_id_2', 'lift_id_6'],
#             'athlete_id_3': ['lift_id_3', 'lift_id_7'],
#         }
#     """
#     athlete_ids = create_athletes
#     competition_ids = create_sessions
#
#     for lift in LIFTS:
#         athlete = list(athlete_ids.keys())[lift["athlete"]]
#         competition = list(competition_ids.keys())[lift["competition"]]
#         lift["athlete"] = Athlete.objects.get(reference_id=athlete)
#         lift.pop("competition", None)
#         created = Lift.objects.create(**lift)
#         competition_ids[competition].append(str(created.reference_id))
#         athlete_ids[athlete].append(str(created.reference_id))
#
#     return {"competition_ids": competition_ids, "athlete_ids": athlete_ids}

################
# Athlete CRUD #
################


@pytest.fixture
def mock_athlete(django_db_blocker) -> dict[str, str | dict[str, str]]:
    """Provide edited athlete data.

    Returns:
        dict[str, str | dict[str, str]]: Athlete result give by a reference id
        and the data provided.
    """
    athlete = {
        "first_name": "Mock",
        "last_name": "Athlete",
        "yearborn": 2000,
    }
    with django_db_blocker.unblock():
        created = Athlete.objects.create(**athlete)
    return {"reference_id": created.reference_id, "data": athlete}


@pytest.fixture
def mock_competition(django_db_blocker) -> dict[str, str | dict[str, str]]:
    """Mock competition data.

    Returns:
        dict[str, str | dict[str, str]]
    """
    competition = {
        "date_start": "2022-01-01",
        "date_end": "2022-01-02",
        "location": "Mock",
        "competition_name": "Competition",
    }
    with django_db_blocker.unblock():
        created = Competition.objects.create(**competition)
    return {"reference_id": created.reference_id, "data": competition}


@pytest.fixture
def mock_lift(
    django_db_blocker, mock_competition, mock_athlete
) -> dict[str, str | dict[str, str]]:
    """Mock lift data.

    Returns:
        dict[str, str | dict[str, str]]
    """
    lift = {
            "competition": Competition.objects.get(reference_id=mock_competition["reference_id"]),
            "athlete": Athlete.objects.get(reference_id=mock_athlete["reference_id"]),
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
            "lottery_number": 3,
            }
    with django_db_blocker.unblock():
        created = Lift.objects.create(**lift)
    return {"reference_id": created.reference_id, "data": lift}
