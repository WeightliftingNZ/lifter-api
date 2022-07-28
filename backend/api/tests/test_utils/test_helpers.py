from datetime import datetime

import pytest

from api.models.utils import age_category, best_lift, ranking_suffixer


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
            },
            id="15 is Youth, Junior, Senior",
        ),
        pytest.param(
            (2022 - 13),
            2022,
            {
                "is_youth": True,
                "is_junior": False,
                "is_senior": False,
                "is_master": False,
            },
            id="13 is Youth",
        ),
        pytest.param(
            (2022 - 35),
            2022,
            {
                "is_youth": False,
                "is_junior": False,
                "is_senior": True,
                "is_master": True,
            },
            id="35 is Senior, Master",
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
