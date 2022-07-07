import pytest

from api.models.utils import ranking_suffixer, best_lift


@pytest.mark.parametrize(
    "test_input,expected",
    [(1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"), (11, "11th"), (101, "101st")],
)
def test_ranking_suffixer(test_input, expected) -> None:
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
def test_best_lift(test_input, expected) -> None:
    """Test best lift."""
    assert best_lift(test_input) == expected
