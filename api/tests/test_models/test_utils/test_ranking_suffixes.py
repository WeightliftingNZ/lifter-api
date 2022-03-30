import pytest

from api.models.utils import rankings


@pytest.fixture
def test_data():
    return [1, 11, 101]


def test_rankings(test_data):
    """Tests if ranking works
    e.g. 1 returns 1st
         11 returns 11th
         101 return 101st
    """
    assert rankings(test_data[0]) == "1st"
    assert rankings(test_data[1]) == "11th"
    assert rankings(test_data[2]) == "101st"
