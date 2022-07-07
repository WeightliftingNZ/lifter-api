"""Test lift endpoints.

Lift retrieve, create, edit and delete.
"""
import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLiftCase:
    """Lift testing."""

    url = "/v1/competitions"

    def test_get_lifts(self, client, mock_lift):
        """Retrieve lifts for a competition."""
        response = client.get(f"{self.url}/{str(mock_lift['data']['competition'].reference_id)}/lifts")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] >= 1
        assert (
            mock_lift["data"]["team"]
            == result["results"][0]["team"]
        )
