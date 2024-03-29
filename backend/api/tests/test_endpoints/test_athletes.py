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
            athlete["reference_id"] for athlete in result["results"]
        ]
        assert set(mock_athlete_ids) == set(result_athlete_ids)

    def test_get_athlete(self, client, athlete_factory):
        """Retrieve a particular athlete by id using the url."""
        athlete = athlete_factory()
        response = client.get(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["first_name"] == athlete.first_name
        assert result["last_name"] == athlete.last_name
        assert result["yearborn"] == athlete.yearborn
        assert result["age_categories"] == athlete.age_categories

    def test_find_athlete(self, client, athlete):
        """Find a athlete using the url search terms."""
        response = client.get(
            f"{self.url}?search={athlete.first_name} {athlete.last_name}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] > 0
        assert result["results"][0]["first_name"] == athlete.first_name

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
                    "full_name": "First Last",
                    "current_grade": None,
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                        "is_master_35_39": False,
                        "is_master_40_44": False,
                        "is_master_45_49": False,
                        "is_master_50_54": False,
                        "is_master_55_59": False,
                        "is_master_60_64": False,
                        "is_master_65_69": False,
                        "is_master_70": False,
                    },
                    "recent_lift": [],
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
        assert result["current_grade"] == expected["current_grade"]
        assert result["recent_lift"] == expected["recent_lift"]
