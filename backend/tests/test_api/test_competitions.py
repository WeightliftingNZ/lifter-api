"""Test competition endpoints.

Competitions to retrieve, create, edit and delete.
"""
import json
import random
from contextlib import nullcontext as does_not_raise
from datetime import datetime, timedelta

import pytest
from django.core import serializers
from django.core.exceptions import ValidationError
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models import Competition, Lift

from ..factories import fake

pytestmark = pytest.mark.django_db


class BaseTestCompetition:
    """Base Test class for Competition testing."""

    url = "/v1/competitions"


class TestCompetitionModel:
    """Testing Competition model functions.

    Includes:
        - Normal CRUD operations.
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
        } == {competition.reference_id for competition in competition_table}

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
            pytest.param(1, does_not_raise(), id="correct-dates"),
            pytest.param(0, does_not_raise(), id="same-day"),
            pytest.param(
                -1,
                pytest.raises(ValidationError, match=r".*date_start.*"),
                id="incorrect-dates",
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
            assert json.loads(
                serializers.serialize("json", [updated_competition])
            )[0].get("fields") != json.loads(
                serializers.serialize("json", [competition])
            )[
                0
            ].get(
                "fields"
            )

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

    def test_search_empty_query(self, batch_competition):
        """Test search manager function with `query=None`."""
        search_result = Competition.objects.search(query=None)
        assert Competition.objects.all().count() == len(batch_competition)
        assert search_result.count() == Competition.objects.all().count()

    @pytest.mark.parametrize(
        "test_inputs",
        [
            pytest.param(("location",), id="location"),
            pytest.param(("name",), id="name"),
            pytest.param(
                (
                    "name",
                    "location",
                ),
                id="name-location",
            ),
        ],
    )
    def test_search(self, competition, batch_competition, test_inputs):
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
    """Test functionality of competition endpoints.

    This includes commonly accessed (not authenticated required):
        - listing many competitions
        - retrieving a competition
        - searching/filtering on competitions

    as well as  higher privileges:
        - creating a competition
        - editing a competition
        - deleting a competition

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
        serialized_competition = json.loads(
            serializers.serialize("json", [competition])
        )[0].get("fields")
        common_keys = set(result.keys() & serialized_competition.keys())
        assert (
            all([result[k] == serialized_competition[k] for k in common_keys])
            is True
        )

    @pytest.mark.parametrize(
        "test_inputs",
        [
            pytest.param(("location",), id="location"),
            pytest.param(("name",), id="name"),
            pytest.param(
                (
                    "name",
                    "location",
                ),
                id="name-location",
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

    def test_find_by_year(self, client, competition_factory):
        """Find competition all in the same year."""
        number_competitions_year = 10
        year = 2021
        for _ in range(number_competitions_year):
            competition_factory.create(
                date_start=fake.date_between_dates(
                    date_start=datetime(year, 1, 1),
                    date_end=datetime(year, 12, 31),
                ),
            )
            competition_factory.create(
                date_start=fake.date_between_dates(
                    date_start=datetime(year - 1, 1, 1),
                    date_end=datetime(year - 1, 12, 31),
                ),
            )
        response = client.get(f"{self.url}?year={year}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == number_competitions_year
        assert (
            Competition.objects.all().count() == number_competitions_year * 2
        )

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_201_CREATED,
                id="admin",
            ),
        ],
    )
    def test_create(self, test_client, expected, competition_factory):
        """Competitions can be created by an admin user and not anon user."""
        competition = competition_factory.stub().__dict__
        response = test_client.post(
            self.url,
            data=competition,
            content_type="application/json",
        )
        assert response.status_code == expected
        competition_exists = Competition.objects.filter(
            reference_id=response.json().get("reference_id")
        ).exists()
        if response.status_code == status.HTTP_201_CREATED:
            assert competition_exists is True
        else:
            assert competition_exists is False

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="admin",
            ),
        ],
    )
    def test_edit(
        self, test_client, expected, competition, competition_factory
    ):
        """Admin users can edit competitions but not anon users."""
        edited_competition = competition_factory.stub()
        response = test_client.patch(
            f"{self.url}/{competition.reference_id}",
            data=edited_competition.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected
        result = response.json()
        current_competition = json.loads(
            serializers.serialize(
                "json",
                [
                    Competition.objects.get(
                        reference_id=competition.reference_id
                    )
                ],
            )
        )[0].get("fields")
        previous_competition = json.loads(
            serializers.serialize("json", [competition])
        )[0].get("fields")

        if response.status_code == status.HTTP_200_OK:
            assert current_competition != previous_competition
            common_keys = set(
                result.keys()
                & current_competition.keys()
                & previous_competition.keys()
            )
            assert (
                all(
                    [result[k] == previous_competition[k] for k in common_keys]
                )
                is False
            )
            assert (
                all([result[k] == current_competition[k] for k in common_keys])
                is True
            )
        else:
            assert current_competition == previous_competition

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_204_NO_CONTENT,
                id="admin",
            ),
        ],
    )
    def test_delete(self, test_client, expected, competition):
        """Admin user can delete competitions, but not anon users."""
        response = test_client.delete(f"{self.url}/{competition.reference_id}")
        assert response.status_code == expected
        count = Competition.objects.filter(
            reference_id=competition.reference_id
        ).count()
        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert count == 0
        else:
            assert count == 1


@pytest.mark.parametrize(
    "test_competition",
    [
        pytest.param(lazy_fixture("competition"), id="competition-no-lifts"),
        pytest.param(
            lazy_fixture("competition_with_lifts"), id="competition-with-lifts"
        ),
    ],
)
class TestCompetitionSerializer(BaseTestCompetition):
    """Tests for CompetitionSerializer."""

    def test_lifts_count(self, client, test_competition):
        """Test lift counts."""
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert (
            result["lifts_count"]
            == Lift.objects.filter(competition=test_competition).count()
        )

    def test_best_lifts(self, client, test_competition):
        """Test best lifts for both men's and women's."""
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        # Provide better validation.
        assert result["best_lifts"] != {}


@pytest.mark.parametrize(
    "test_competition",
    [
        pytest.param(
            lazy_fixture("competition_with_lifts"),
            id="competition-with-lifts",
        ),
        pytest.param(lazy_fixture("competition"), id="competition-no-lifts"),
    ],
)
class TestCompetitionDetailSerializer(BaseTestCompetition):
    """Test for CompetitionDetailSerializer."""

    def test_competition_last_edited(self, client, test_competition):
        """Provide the last edit for a competition."""
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[
            "competition_last_edited"
        ] == test_competition.history_record.latest().history_date.isoformat().replace(
            "+00:00", "Z"
        )

    def test_competition_last_edited_missing(self, client, test_competition):
        """Handle missing history data for competition."""
        test_competition.history_record.all().delete()
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["competition_last_edited"] is None

    def test_lift_last_edited(self, client, test_competition):
        """Provide the last edit for a competition lift."""
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        lift_histories = [
            lift.history_record.latest().history_date
            for lift in test_competition.lift_set.all()
        ]
        if len(lift_histories) != 0:
            assert result["lift_last_edited"] == sorted(lift_histories)[
                -1
            ].isoformat().replace("+00:00", "Z")
        else:
            assert result["lift_last_edited"] is None

    def test_lift_set(self, client, test_competition):
        """Test the lift set for an athlete."""
        response = client.get(f"{self.url}/{test_competition.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert {lift["reference_id"] for lift in result["lift_set"]} == {
            lift["reference_id"] for lift in test_competition.lift_set.values()
        }
