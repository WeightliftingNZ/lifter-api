"""Test competition endpoints.

Competitions to retrieve, create, edit and delete.
"""
from contextlib import nullcontext as does_not_raise

import pytest
from django.core.exceptions import ValidationError
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
        mock_competition_ids = [comp.reference_id for comp in mock_competition]
        result_competition_ids = [
            comp["reference_id"] for comp in result["results"]
        ]
        assert set(mock_competition_ids) == set(result_competition_ids)

    def test_get_competition(self, client, mock_competition):
        """Retrieve a particular competition."""
        response = client.get(f"{self.url}/{mock_competition[0].reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert (
            mock_competition[0].competition_name == result["competition_name"]
        )

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
            (
                {
                    # invalid `date_start`
                    "date_start": "2022-13-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "competition_name": "Competition",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_admin_create_competition(
        self, admin_client, test_input, expected
    ):
        """Admin users can create competitions."""
        response = admin_client.post(
            self.url, data=test_input, content_type="application/json"
        )
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "date_start": "2022-01-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "competition_name": "Competition",
                },
                does_not_raise(),
                id="Normal input.",
            ),
            pytest.param(
                {
                    "date_start": "2022-01-03",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "competition_name": "Competition",
                },
                pytest.raises(
                    ValidationError,
                    match="Start date must be before the end date.",
                ),
                id="`date_start` after `date_end`.",
            ),
        ],
    )
    def test_create_competition_custom_validation(
        self, admin_client, test_input, expected
    ):
        """Test custom validation for competition creation."""
        with expected:
            response = admin_client.post(
                self.url, data=test_input, content_type="application/json"
            )
            assert response is not None

    def test_anon_create_competition(self, client):
        """Anonymous users cannot create competitions."""
        response = client.post(
            self.url, data={}, content_type="application/json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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
        response = admin_client.patch(
            f"{self.url}/{mock_competition[0].reference_id}",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    def test_anon_edit_competition(self, client, mock_competition):
        """Anon user cannot edit a competition."""
        anon_response = client.patch(
            f"{self.url}/{mock_competition[0].reference_id}",
            data={},
            content_type="application/json",
        )
        assert anon_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_delete_competition(self, admin_client, mock_competition):
        """Admin user can delete competitions."""
        response = admin_client.delete(
            f"{self.url}/{mock_competition[0].reference_id}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_anon_delete_competition(self, client, mock_competition):
        """Anonymous users cannot delete competitions."""
        response = client.delete(
            f"{self.url}/{mock_competition[0].reference_id}"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_competition_custom_payload(self, client, mock_lift):
        """Test competition custom payload."""
        IDX = 0
        competition_id = mock_lift[IDX].competition.reference_id
        response = client.get(f"{self.url}/{str(competition_id)}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["lifts_count"] == len(
            [
                lift
                for lift in mock_lift
                if lift.competition.reference_id == competition_id
            ]
        )
