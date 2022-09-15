from datetime import datetime

import pytest
from rest_framework import status

from api.models.athletes import MINIMUM_YEAR_FROM_BIRTH

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
        mock_athlete_ids = [
            str(athlete.reference_id) for athlete in mock_athlete
        ]
        result_athlete_ids = [
            comp["reference_id"] for comp in result["results"]
        ]
        assert set(mock_athlete_ids) == set(result_athlete_ids)

    def test_get_athlete(self, client, mock_athlete):
        """Retrieve a particular athlete by id using the url."""
        response = client.get(f"{self.url}/{mock_athlete[0].reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["last_name"] == mock_athlete[0].last_name

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                "&search={}",
                2,
                id="2 match for name",
            ),
        ],
    )
    def test_find_athlete(self, client, mock_athlete, test_input, expected):
        """Find a athlete using the url search terms."""
        response = client.get(
            f"{self.url}?search={mock_athlete[0].first_name} {mock_athlete[0].last_name}"
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
            (
                {
                    # missing `first_name`
                    "last_name": "InCorrect",
                    "yearborn": 1900,
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )
    def test_admin_create_athlete(self, admin_client, test_input, expected):
        """Admin user can create athletes."""
        response = admin_client.post(
            self.url, data=test_input, content_type="application/json"
        )
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "first_name": "Athlete",
                    "last_name": "Correct",
                    "yearborn": 1900,
                },
                status.HTTP_201_CREATED,
                id="Normal input.",
            ),
            pytest.param(
                {
                    "first_name": "Athlete",
                    "last_name": "OldEnough",
                    "yearborn": datetime.now().year - MINIMUM_YEAR_FROM_BIRTH,
                },
                status.HTTP_201_CREATED,
            ),
            pytest.param(
                {
                    "first_name": "Athlete",
                    "last_name": "TooYoung",
                    "yearborn": datetime.now().year
                    - (MINIMUM_YEAR_FROM_BIRTH - 1),
                },
                status.HTTP_400_BAD_REQUEST,
                id="`yearborn` after acceptable year.",
            ),
        ],
    )
    def test_create_athlete_custom_validation(
        self, admin_client, test_input, expected
    ):
        """Test custom validation for competition creation."""
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
            f"{self.url}/{mock_athlete[0].reference_id}",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    def test_anon_edit_athlete(self, client, mock_athlete):
        """Anon users cannot edit athletes."""
        anon_response = client.patch(
            f"{self.url}/{mock_athlete[0].reference_id}",
            data={},
            content_type="application/json",
        )
        assert anon_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_delete_athlete(self, admin_client, mock_athlete):
        """Admin users can delete athletes."""
        response = admin_client.delete(
            f"{self.url}/{mock_athlete[0].reference_id}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_anon_delete_athlete(self, client, mock_athlete):
        """Anonymous users cannot delete athletes."""
        response = client.delete(f"{self.url}/{mock_athlete[0].reference_id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "first_name": "First",
                    "last_name": "Last",
                    "yearborn": datetime.now().year - 21,
                },
                {
                    "full_name": "LAST, First",
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                id="Normal",
            )
        ],
    )
    def test_athlete_payload_custom_properties(
        self, admin_client, test_input, expected
    ):
        """Test athlete payload for custom properties."""
        response = admin_client.post(
            self.url, data=test_input, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["full_name"] == expected["full_name"]
        assert result["age_categories"] == expected["age_categories"]
