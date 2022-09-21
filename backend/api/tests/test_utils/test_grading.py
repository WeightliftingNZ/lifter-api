import pytest

from api.models.utils import determine_grade


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(("M96", 232), "C", id="M96 - A"),
        pytest.param(("M49", 188), "A", id="M49 - A"),
        pytest.param(("W59", 184), "Elite", id="W59 - Elite"),
        pytest.param(("W59", 95), None, id="W59 - No grade"),
    ],
)
def test_determine_grade(test_input, expected):
    """Determine grade for a lifter."""
    assert (
        determine_grade(
            weight_category=test_input[0], total_lifted=test_input[1]
        )
        == expected
    )
