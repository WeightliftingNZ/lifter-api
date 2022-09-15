"""Test competition  endpoints.

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
        assert mock_competition[0].name == result["name"]

    def test_find_competition_by_date(self, client, mock_competition):
        """Find a competition by date.

        To consider: there are 2 mocked competitions (this is assumed), and if that is changed, it will likely result in the test failing.
            - mocked competition different dates.
            - one competition is set to today's date.
            - the second competition is set to a date in 2019.
        """
        # competition one - today's date
        one_response = client.get(
            f"{self.url}?date_start_after={mock_competition[0].date_start}&date_start_before={mock_competition[0].date_start}&search=&ordering="
        )
        assert one_response.status_code == status.HTTP_200_OK
        one_result = one_response.json()
        assert one_result["count"] == 1

        # all competitions - searching between date of earliest competition to today
        all_response = client.get(
            f"{self.url}?date_start_after={mock_competition[1].date_start}&date_start_before={mock_competition[0].date_start}&search=&ordering="
        )
        assert all_response.status_code == status.HTTP_200_OK
        all_result = all_response.json()
        assert all_result["count"] == len(mock_competition)

    def test_find_competition_by_search(self, client, mock_competition):
        """Find a competition by search.

        To consider: there are 2 mocked competitions (this is assumed), and if that is changed, it will likely result in the test failing.
            - mocked competition have unique names, but same location.
            - `name` search for this test will return only 1 competition.
            - `location` search will return 2 competitions.
        """
        # name
        response = client.get(
            f"{self.url}?date_start_after=&date_start_before=&search={mock_competition[0].name}&ordering="
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == 1

        # location
        response = client.get(
            f"{self.url}?date_start_after=&date_start_before=&search={mock_competition[0].location}&ordering="
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == len(mock_competition)

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            (
                {
                    "date_start": "2022-01-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "name": "Competition",
                },
                status.HTTP_201_CREATED,
            ),
            (
                {
                    # invalid `date_start`
                    "date_start": "2022-13-01",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "name": "Competition",
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
                    "name": "Competition",
                },
                does_not_raise(),
                id="Normal input.",
            ),
            pytest.param(
                {
                    "date_start": "2022-01-03",
                    "date_end": "2022-01-02",
                    "location": "Mock",
                    "name": "Competition",
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
                    "name": "Edited Name",
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
