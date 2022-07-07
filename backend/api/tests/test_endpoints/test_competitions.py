"""Test competition endpoints.

Competitions to retrieve, create, edit and delete.
"""
import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCompetitionCase:
    """Competition testing."""

    url = "/v1/competitions"

    def test_get_competitions(self, client, mock_competition):
        """Retrieve competitions."""
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] >= 1
        assert (
            mock_competition["data"]["competition_name"]
            == result["results"][0]["competition_name"]
        )

    def test_get_competition(self, client, mock_competition):
        """Retrieve a particular competition."""
        response = client.get(f"{self.url}/{mock_competition['reference_id']}")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.skip("There is no find functionality!")
    def test_find_competition(self):
        """Find a competition."""
        # TODO: this functionality does not exist yet
        pass

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (
                {
                    "date_start": "2022-01-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "competition_name": "Competition",
                },
                status.HTTP_201_CREATED,
            ),
            pytest.param(
                {
                    # invalid `date_start`
                    "date_start": "2022-13-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "competition_name": "Competition",
                },
                status.HTTP_400_BAD_REQUEST,
                marks=pytest.mark.xfail,
            ),
        ],
    )
    def test_create_competition(self, admin_client, test_input, expected):
        """Admin users can create competitions."""
        response = admin_client.post(
            self.url, data=test_input, content_type="application/json"
        )
        assert response.status_code == expected

    def test_anon_create_competition(self, client):
        """Anonymous users cannot create competitions."""
        anon_response = client.post(
            self.url, data={}, content_type="application/json"
        )
        assert anon_response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (
                {
                    "competition_name": "Edited Name",
                },
                status.HTTP_200_OK,
            ),
            (
                {
                    "date_end": "ThisIsNotDate",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_admin_edit_competition(
        self, admin_client, test_input, expected, mock_competition
    ):
        """Admin user can edit a competition."""
        admin_response = admin_client.patch(
            f"{self.url}/{mock_competition['reference_id']}",
            data=test_input,
            content_type="application/json",
        )
        assert admin_response.status_code == expected

    def test_anon_edit_competition(self, client, mock_competition):
        """Anon user cannot edit a competition."""
        anon_response = client.patch(
            f"{self.url}/{mock_competition['reference_id']}",
            data={},
            content_type="application/json",
        )
        assert anon_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_delete_competition(self, admin_client, mock_competition):
        """Admin user can delete competitions."""
        response = admin_client.delete(
            f"{self.url}/{mock_competition['reference_id']}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_anon_delete_competition(self, client, mock_competition):
        """Anonymous users cannot delete competitions."""
        response = client.delete(
            f"{self.url}/{mock_competition['reference_id']}"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
