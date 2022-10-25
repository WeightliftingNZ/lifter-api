from contextlib import nullcontext as does_not_raise
from datetime import datetime
from decimal import Decimal as D

import pytest
from django.core.exceptions import ValidationError

from api.models.utils import (
    age_category,
    best_lift,
    calculate_sinclair,
    ranking_suffixer,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(1, "1st"),
        pytest.param(2, "2nd"),
        pytest.param(3, "3rd"),
        pytest.param(4, "4th"),
        pytest.param(11, "11th"),
        pytest.param(101, "101st", id="101st"),
        pytest.param(
            11, "11st", marks=pytest.mark.xfail, id="Can't have 11st"
        ),
    ],
)
def test_ranking_suffixer(test_input, expected):
    """Test rank output.

    e.g. 1 returns 1st
         11 returns 11th
         101 return 101st
    """
    assert ranking_suffixer(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "1st": {"lift_status": "LIFT", "weight": 100},
                "2nd": {
                    "lift_status": "NOLIFT",
                    "weight": 101,
                },
                "3rd": {
                    "lift_status": "NOLIFT",
                    "weight": 101,
                },
            },
            ("1st", 100),
        ),
        (
            {
                "1st": {"lift_status": "LIFT", "weight": 100},
                "2nd": {
                    "lift_status": "LIFT",
                    "weight": 101,
                },
                "3rd": {
                    "lift_status": "NOLIFT",
                    "weight": 101,
                },
            },
            ("2nd", 101),
        ),
    ],
)
def test_best_lift(test_input, expected):
    """Test best lift."""
    assert best_lift(test_input) == expected


@pytest.mark.parametrize(
    "test_input_yearborn,test_input_competition_year,expected",
    [
        pytest.param(
            datetime.now().year - 15,
            None,
            {
                "is_youth": True,
                "is_junior": True,
                "is_senior": True,
                "is_master": False,
                "is_master_35_39": False,
                "is_master_40_44": False,
                "is_master_45_49": False,
                "is_master_50_54": False,
                "is_master_55_59": False,
                "is_master_60_64": False,
                "is_master_65_69": False,
                "is_master_70": False,
            },
            id="youth-junior-senior-15",
        ),
        pytest.param(
            (2022 - 13),
            2022,
            {
                "is_youth": True,
                "is_junior": False,
                "is_senior": False,
                "is_master": False,
                "is_master_35_39": False,
                "is_master_40_44": False,
                "is_master_45_49": False,
                "is_master_50_54": False,
                "is_master_55_59": False,
                "is_master_60_64": False,
                "is_master_65_69": False,
                "is_master_70": False,
            },
            id="youth-13",
        ),
        pytest.param(
            (2022 - 35),
            2022,
            {
                "is_youth": False,
                "is_junior": False,
                "is_senior": True,
                "is_master": True,
                "is_master_35_39": True,
                "is_master_40_44": False,
                "is_master_45_49": False,
                "is_master_50_54": False,
                "is_master_55_59": False,
                "is_master_60_64": False,
                "is_master_65_69": False,
                "is_master_70": False,
            },
            id="senior-master-35",
        ),
        pytest.param(
            (2022 - 30),
            2022,
            {
                "is_youth": False,
                "is_junior": False,
                "is_senior": True,
                "is_master": False,
                "is_master_35_39": False,
                "is_master_40_44": False,
                "is_master_45_49": False,
                "is_master_50_54": False,
                "is_master_55_59": False,
                "is_master_60_64": False,
                "is_master_65_69": False,
                "is_master_70": False,
            },
            id="senior-30",
        ),
        pytest.param(
            (2022 - 70),
            2022,
            {
                "is_youth": False,
                "is_junior": False,
                "is_senior": True,
                "is_master": True,
                "is_master_35_39": False,
                "is_master_40_44": False,
                "is_master_45_49": False,
                "is_master_50_54": False,
                "is_master_55_59": False,
                "is_master_60_64": False,
                "is_master_65_69": False,
                "is_master_70": True,
            },
            id="senior-master-70",
        ),
    ],
)
def test_age_category(
    test_input_yearborn, test_input_competition_year, expected
):
    """Test age category."""
    if test_input_competition_year is None:
        assert age_category(yearborn=test_input_yearborn) == expected
    else:
        assert (
            age_category(
                yearborn=test_input_yearborn,
                competition_year=test_input_competition_year,
            )
            == expected
        )


@pytest.mark.parametrize(
    "test_input,exception",
    [
        pytest.param((1990, 2000), does_not_raise(), id="Normal Input"),
        pytest.param(
            (2000, 1990),
            pytest.raises(
                ValidationError,
                match=f"Age of athlete is negative: {1990-2000}",
            ),
            id="Exception",
        ),
    ],
)
def test_age_category_error(test_input, exception):
    """Testing exception."""
    with exception:
        age_category(yearborn=test_input[0], competition_year=test_input[1])


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(
            {
                "bodyweight": 90.9,
                "total_lifted": 303,
                "weight_category": "W87+",
                "yearborn": 1990,
                "lift_year": 2020,
            },
            332.787,
            id="W87+",
        ),
        pytest.param(
            {
                "bodyweight": 56,
                "total_lifted": 307,
                "weight_category": "M61",
                "yearborn": 1990,
                "lift_year": 2020,
            },
            470.122,
            id="M61",
        ),
        pytest.param(
            {
                "bodyweight": 48,
                "total_lifted": 217,
                "weight_category": "W49",
                "yearborn": 1990,
                "lift_year": 2020,
            },
            343.964,
            id="W49",
        ),
    ],
)
def test_calculate_sinclair(test_input, expected):
    """Calculate sinclair."""
    assert calculate_sinclair(**test_input) == round(D(expected), 3)
