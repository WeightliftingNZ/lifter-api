"""Testing search functionality - combined search."""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestSearch:
    """Testing combined search."""

    url = "/v1/search"

    @pytest.mark.parametrize(
        "test_input,expected", [pytest.param("&q=", None, id="empty_search")]
    )
    def test_get_search(self, client, test_input, expected):
        """Ensure search endpoint works."""
        response = client.get(f"{self.url}/{test_input}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] >= 1
