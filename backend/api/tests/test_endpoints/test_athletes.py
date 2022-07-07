"""Test athlete endpoints.

Athletes to retrieve, create, edit and delete.
"""
import pytest
from rest_framework import status

from api.models import Athlete

pytestmark = pytest.mark.django_db


class TestAthleteCase:
    """Athlete testing."""

    url = "/v1/athletes"

    def test_get_athletes(self, client, mock_athlete):
        """Retrieve athletes."""
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] >= 1
        assert (
            mock_athlete["data"]["last_name"]
            == result["results"][0]["last_name"]
        )

    def test_get_athlete(self, client, mock_athlete):
        """Retrieve a particular athlete by id using the url."""
        response = client.get(f"{self.url}/{mock_athlete['reference_id']}")
        assert response.status_code == status.HTTP_200_OK

    def test_find_athlete(self, client, mock_athlete):
        """Find a athlete using the url search terms."""
        response = client.get(
            f"{self.url}?search={mock_athlete['data']['first_name']}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] > 0

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (
                {
                    "first_name": "Athlete",
                    "last_name": "Correct",
                    "yearborn": 1900,
                },
                status.HTTP_201_CREATED,
            ),
            pytest.param(
                {
                    # missing `first_name`
                    "last_name": "InCorrect",
                    "yearborn": 1900,
                },
                status.HTTP_400_BAD_REQUEST,
                marks=pytest.mark.xfail,
            ),
        ],
    )
    def test_admin_create_athlete(self, admin_client, test_input, expected):
        """Admin user can create athletes."""
        response = admin_client.post(
            self.url, data=test_input, content_type="application/json"
        )
        assert response.status_code == expected

    def test_anon_create_athlete(self, client):
        """Anon users cannot create athletes."""
        response = client.post(
            self.url, data={}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (
                {
                    "last_name": "Edited",
                },
                status.HTTP_200_OK,
            ),
            (
                {
                    # yearborn only accepts integers
                    "yearborn": "ThisIsNotANumber",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_admin_edit_athlete(
        self, test_input, expected, admin_client, mock_athlete
    ):
        """Admin users can edit athletes."""
        response = admin_client.patch(
            f"{self.url}/{mock_athlete['reference_id']}",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    def test_anon_edit_athlete(self, client, mock_athlete):
        """Anon users cannot edit athletes."""
        anon_response = client.patch(
            f"{self.url}/{mock_athlete['reference_id']}",
            data={},
            content_type="application/json",
        )
        assert anon_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_delete_athlete(self, admin_client, mock_athlete):
        """Admin users can delete athletes."""
        response = admin_client.delete(
            f"{self.url}/{mock_athlete['reference_id']}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_anon_delete_athlete(self, client, mock_athlete):
        """Anonymous users cannot delete athletes."""
        response = client.delete(f"{self.url}/{mock_athlete['reference_id']}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            Athlete.objects.filter(
                reference_id=str(mock_athlete.get("reference_id"))
            ).exists()
            is True
        )
