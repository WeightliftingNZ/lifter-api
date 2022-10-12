"""Test competition  endpoints.

Competitions to retrieve, create, edit and delete.
"""
import random
from contextlib import nullcontext as does_not_raise
from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models import Competition

from .factories import fake

pytestmark = pytest.mark.django_db


class BaseTestCompetition:
    """Base Test class for Competition testing."""

    url = "/v1/competitions"


class TestCompetitionModel:
    """Testing Competition model functions.

    Includes:
        - Normal CRUD operations.
        - Custom properties:
            -
        - Validation:
            - `date_start` must be before `date_end`
    """

    def test_instance(self, competition):
        """Ensure the created instance is a Competition model instance."""
        assert isinstance(competition, Competition)

    def test_all(self, batch_competition):
        """Can retrieve entire Competition table."""
        competition_table = Competition.objects.all()
        assert competition_table.count() == len(batch_competition)
        assert {
            competition.reference_id for competition in batch_competition
        } == {competition.reference_id for competition in batch_competition}

    def test_get(self, competition, batch_competition):
        """Can retrieve a single competition."""
        retrieved_competition = Competition.objects.filter(
            reference_id=competition.reference_id
        )
        assert retrieved_competition.exists() is True
        assert retrieved_competition.first().reference_id not in [
            competition.reference_id for competition in batch_competition
        ]

    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(1, does_not_raise(), id="model-create-correct-dates"),
            pytest.param(0, does_not_raise(), id="model-create-same-day"),
            pytest.param(
                -1,
                pytest.raises(ValidationError, match=r".*date_start.*"),
                id="model-create-incorrect-dates",
            ),
        ],
    )
    def test_create(self, competition_factory, test_input, exception):
        """Able to create a competition.

        Also tests `date_start` and `date_end` validation.
        """
        date_start = fake.date_object()
        date_end = (
            date_start + timedelta(days=random.randint(1, 3)) * test_input
        )
        with exception:
            competition = Competition.objects.create(
                **competition_factory.stub(
                    date_start=date_start, date_end=date_end
                ).__dict__
            )
            assert (
                Competition.objects.filter(
                    reference_id=competition.reference_id
                ).exists()
                is True
            )

    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(1, does_not_raise(), id="model-create-correct-dates"),
            pytest.param(0, does_not_raise(), id="model-create-same-day"),
            pytest.param(
                -1,
                pytest.raises(ValidationError, match=r".*date_start.*"),
                id="model-create-incorrect-dates",
            ),
        ],
    )
    def test_update(
        self, competition, competition_factory, test_input, exception
    ):
        """Able to update competition.

        Also tests `date_start` and `date_end` validation.
        """
        date_start = fake.date_object()
        date_end = (
            date_start + timedelta(days=random.randint(1, 3)) * test_input
        )
        updated_competition = Competition.objects.get(
            reference_id=competition.reference_id
        )
        new_details = competition_factory.stub(
            date_start=date_start, date_end=date_end
        ).__dict__
        for attr, value in new_details.items():
            setattr(updated_competition, attr, value)
        with exception:
            updated_competition.save()
            assert updated_competition.name != competition.name
            assert updated_competition.location != competition.location
            assert updated_competition.date_start != competition.date_start
            assert updated_competition.date_end != competition.date_end

    def test_delete(self, competition):
        """Test competition deletion.

        In the future, this will be made into a soft delete.
        """
        Competition.objects.get(reference_id=competition.reference_id).delete()
        assert (
            Competition.objects.filter(
                reference_id=competition.reference_id
            ).exists()
            is False
        )


class TestCompetitionManager:
    """Competition custom manager functionality tests."""

    def test_search_query_none(self, batch_competition):
        """Test search manager function with `query=None`."""
        search_result = Competition.objects.search(query=None)
        assert Competition.objects.all().count() == len(batch_competition)
        assert search_result.count() == Competition.objects.all().count()

    @pytest.mark.parametrize(
        "test_inputs",
        [
            pytest.param(("location",), id="search-location"),
            pytest.param(("name",), id="search-name"),
            pytest.param(
                (
                    "name",
                    "location",
                ),
                id="search-name-location",
            ),
        ],
    )
    def test_search_query(self, competition, batch_competition, test_inputs):
        """Testing search query."""
        search_result = Competition.objects.search(
            query=" ".join(
                [
                    getattr(competition, test_input)
                    for test_input in test_inputs
                ]
            )
        )
        assert Competition.objects.all().count() == len(batch_competition) + 1
        assert search_result.count() < len(batch_competition) + 1
        assert competition.reference_id in {
            result.reference_id for result in search_result
        }


class TestCompetitionEndpoints(BaseTestCompetition):
    """Test functionality of endpoints.

    This includes commonly accessed (not authenticated required):
        - listing many athletes
        - retrieving an athlete
        - searching/filtering on athletes

    as well as  higher privileges:
        - creating an athlete
        - editing an athlete
        - deleting an athlete

    Higher privileged actions require administration level, but in the future \
            this will be moved to a group.
    """

    def test_list(self, client, batch_competition):
        """List competitions."""
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == len(batch_competition)

    def test_retrieve(self, client, competition):
        """Retrieve athlete."""
        response = client.get(f"{self.url}/{competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["name"] == competition.name

    @pytest.mark.parametrize(
        "test_inputs",
        [
            pytest.param(("location",), id="search-location"),
            pytest.param(("name",), id="search-name"),
            pytest.param(
                (
                    "name",
                    "location",
                ),
                id="search-name-location",
            ),
        ],
    )
    def test_filter_by_search(
        self, client, competition, batch_competition, test_inputs
    ):
        """List and retrieve competition by filter."""
        response = client.get(
            f"{self.url}?search={' '.join([getattr(competition, test_input) for test_input in test_inputs])}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] > 0
        assert competition.reference_id in {
            competition["reference_id"] for competition in result["results"]
        }

    def test_find_by_date(self, client, competition, batch_competition):
        """Find a competition by date."""
        response = client.get(
            f"{self.url}?date_start_after={competition.date_start}&date_start_before={competition.date_start}&search=&ordering="
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert competition.reference_id in {
            competition["reference_id"] for competition in result["results"]
        }

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="athlete-create-anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_201_CREATED,
                id="athlete-create-admin",
            ),
        ],
    )
    def test_create(self, test_client, expected, competition_factory):
        """Competitions can be created by an admin user and not anon user."""
        competition = competition_factory.stub()
        response = test_client.post(
            self.url,
            data=competition.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected
        count = Competition.objects.filter(
            reference_id=response.json().get("reference_id")
        ).count()
        if response.status_code == status.HTTP_201_CREATED:
            assert count == 1
        else:
            assert count == 0

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
