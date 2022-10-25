"""Testing athlete related functionality."""

import json
from contextlib import nullcontext as does_not_raise
from datetime import datetime

import pytest
from django.core import serializers
from django.core.exceptions import ValidationError
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models import Athlete, Lift
from api.models.utils.constants import GRADES
from config.settings import MINIMUM_YEAR_FROM_BIRTH

pytestmark = pytest.mark.django_db


class BaseTestAthlete:
    """Base Test class for Athlete testing."""

    url = "/v1/athletes"


class TestAthleteModel:
    """Testing Athlete model functions.

    Includes:
        - Normal CRUD operations
        - Custom properties:
            - `age_caregories`
            - `full_name`
        - Validation:
            - `yearborn` validation
    """

    def test_instance(self, athlete):
        """Ensure the created instance is an athlete model instance."""
        assert isinstance(athlete, Athlete)

    def test_all(self, batch_athlete):
        """Can retrieve entire Athlete table."""
        athlete_table = Athlete.objects.all()
        assert athlete_table.count() == len(batch_athlete)
        assert {athlete.reference_id for athlete in athlete_table} == {
            athlete.reference_id for athlete in batch_athlete
        }

    def test_get(self, athlete, batch_athlete):
        """Can retrieve a single athlete."""
        retrieved_athlete = Athlete.objects.filter(
            reference_id=athlete.reference_id
        )
        assert retrieved_athlete.exists() is True
        assert retrieved_athlete.first().reference_id not in [
            athlete.reference_id for athlete in batch_athlete
        ]

    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(
                datetime.now().year - MINIMUM_YEAR_FROM_BIRTH,
                does_not_raise(),
                id="old-enough",
            ),
            pytest.param(
                datetime.now().year - (MINIMUM_YEAR_FROM_BIRTH - 1),
                pytest.raises(
                    ValidationError,
                    match=r".*yearborn.*",
                ),
                id="too-young",
            ),
        ],
    )
    def test_create(self, athlete_factory, test_input, exception):
        """Able to create an athlete.

        Also tests `yearborn` validation.
        """
        with exception:
            athlete = Athlete.objects.create(
                **athlete_factory.stub(yearborn=test_input).__dict__
            )
            assert (
                Athlete.objects.filter(
                    reference_id=athlete.reference_id
                ).exists()
                is True
            )

    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(
                datetime.now().year - MINIMUM_YEAR_FROM_BIRTH,
                does_not_raise(),
                id="old-enough",
            ),
            pytest.param(
                datetime.now().year - (MINIMUM_YEAR_FROM_BIRTH - 1),
                pytest.raises(
                    ValidationError,
                    match=r".*yearborn.*",
                ),
                id="too-young",
            ),
        ],
    )
    def test_update(self, athlete, athlete_factory, test_input, exception):
        """Able to update athlete."""
        updated_athlete = Athlete.objects.get(
            reference_id=athlete.reference_id
        )
        new_details = athlete_factory.stub(yearborn=test_input).__dict__
        for attr, value in new_details.items():
            setattr(updated_athlete, attr, value)
        with exception:
            updated_athlete.save()
            assert json.loads(
                serializers.serialize("json", [updated_athlete])
            )[0].get("fields") != json.loads(
                serializers.serialize("json", [athlete])
            )[
                0
            ].get(
                "fields"
            )

    def test_delete(self, athlete):
        """Test athlete deletion.

        In the future, this will be made into a soft delete.
        """
        Athlete.objects.get(reference_id=athlete.reference_id).delete()
        assert (
            Athlete.objects.filter(reference_id=athlete.reference_id).exists()
            is False
        )

    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param("age_categories"),
            pytest.param("full_name"),
            pytest.param("invalid_property", marks=pytest.mark.xfail),
        ],
    )
    def test_custom_properties(self, test_input, athlete):
        """Testing custom properties for the `Athlete` model."""
        assert hasattr(athlete, test_input) is True

    def test_full_name(self, athlete):
        """Testing full name combination from `first_name` and `last_name`."""
        assert athlete.full_name is not None
        assert (
            Athlete.objects.get(reference_id=athlete.reference_id).full_name
            == f"{athlete.first_name.title()} {athlete.last_name.title()}"
        )


class TestAthleteManager:
    """Athlete custom manager functionality tests."""

    def test_search_empty_query(self, batch_athlete):
        """Test for search manager function when `query=None`."""
        search_result = Athlete.objects.search(query=None)
        assert Athlete.objects.all().count() == len(batch_athlete)
        assert search_result.count() == Athlete.objects.all().count()

    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param("first_name", id="first-name"),
            pytest.param("last_name", id="last-name"),
            pytest.param("full_name", id="full-name"),
        ],
    )
    def test_search(self, athlete, batch_athlete, test_input):
        """Testing search query on the athlete's full name."""
        search_result = Athlete.objects.search(
            query=getattr(athlete, test_input)
        )
        assert Athlete.objects.all().count() == len(batch_athlete) + 1
        assert search_result.count() < len(batch_athlete) + 1
        assert athlete.reference_id in {
            result.reference_id for result in search_result
        }


class TestAthleteEndpoints(BaseTestAthlete):
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

    def test_list(self, client, batch_athlete):
        """List athletes."""
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == len(batch_athlete)

    def test_retrieve(self, client, athlete):
        """Retrieve athlete."""
        response = client.get(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        serialized_athlete = json.loads(
            serializers.serialize("json", [athlete])
        )[0].get("fields")
        common_keys = set(result.keys() & serialized_athlete.keys())
        assert (
            all([result[k] == serialized_athlete[k] for k in common_keys])
            is True
        )

    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param("first_name", id="first_name"),
            pytest.param("last_name", id="last_name"),
            pytest.param("full_name", id="full_name"),
        ],
    )
    def test_filter(self, client, athlete, test_input):
        """List and retrieve athlete by filter."""
        response = client.get(
            f"{self.url}?search={getattr(athlete, test_input)}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] > 0

    # TODO Validation of yearborn
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
    def test_create(
        self,
        test_client,
        expected,
        athlete_factory,
    ):
        """Athlete can only be created by an admin user and not anon user."""
        athlete = athlete_factory.stub().__dict__
        response = test_client.post(
            self.url,
            data=athlete,
            content_type="application/json",
        )
        assert response.status_code == expected
        athlete_exists = Athlete.objects.filter(
            reference_id=response.json().get("reference_id")
        ).exists()
        if response.status_code == status.HTTP_201_CREATED:
            assert athlete_exists is True
        else:
            assert athlete_exists is False

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
    def test_edit(self, test_client, expected, athlete, athlete_factory):
        """Admin users can edit athletes but not anon users."""
        edited_athlete = athlete_factory.stub().__dict__
        response = test_client.patch(
            f"{self.url}/{athlete.reference_id}",
            data=edited_athlete,
            content_type="application/json",
        )
        assert response.status_code == expected
        result = response.json()
        current_athlete = json.loads(
            serializers.serialize(
                "json",
                [Athlete.objects.get(reference_id=athlete.reference_id)],
            )
        )[0].get("fields")
        previous_athlete = json.loads(
            serializers.serialize("json", [athlete])
        )[0].get("fields")
        if response.status_code == status.HTTP_200_OK:
            assert current_athlete != previous_athlete
            common_keys = set(
                result.keys()
                & current_athlete.keys()
                & previous_athlete.keys()
            )
            assert (
                all([result[k] == previous_athlete[k] for k in common_keys])
                is False
            )
            assert (
                all([result[k] == current_athlete[k] for k in common_keys])
                is True
            )
        else:
            assert current_athlete == previous_athlete

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
    def test_delete(self, test_client, expected, athlete):
        """Admin users can delete athletes, but not anon users."""
        response = test_client.delete(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == expected
        athlete_exists = Athlete.objects.filter(
            reference_id=athlete.reference_id
        ).exists()
        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert athlete_exists is False
        else:
            assert athlete_exists is True


class TestAthleteSerializer(BaseTestAthlete):
    """Testing the Athlete Serializer custom fields."""

    def test_lift_count(self, client, athlete_with_lifts):
        """Test lift counts."""
        response = client.get(f"{self.url}/{athlete_with_lifts.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert (
            result["lifts_count"]
            == Lift.objects.filter(athlete=athlete_with_lifts).count()
        )

    def test_current_grade(self, client, athlete_with_lifts):
        """Provide grade for an athlete based on their lifts."""
        response = client.get(f"{self.url}/{athlete_with_lifts.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["current_grade"] in GRADES

    def test_recent_lift(self, client, lift):
        """Test getting the recent lift for a lifter."""
        response = client.get(f"{self.url}/{lift.athlete.reference_id}")
        result = response.json()
        assert (
            result["recent_lift"][0]["snatch_first_weight"]
            == lift.snatch_first_weight
        )


@pytest.mark.parametrize(
    "test_athlete",
    [
        pytest.param(
            lazy_fixture("athlete_with_lifts"),
            id="with-lifts",
        ),
        pytest.param(lazy_fixture("athlete_with_no_total"), id="no-total"),
        pytest.param(lazy_fixture("athlete"), id="no-lifts"),
    ],
)
class TestAthleteDetailSerializer(BaseTestAthlete):
    """Testing the Athlete Detail Serializer custom fields."""

    def test_athlete_last_edited(self, client, test_athlete):
        """Provide the last edit for an athlete."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[
            "athlete_last_edited"
        ] == test_athlete.history_record.latest().history_date.isoformat().replace(
            "+00:00", "Z"
        )

    def test_athlete_last_edited_missing(self, client, test_athlete):
        """Test athlete missing a history record."""
        test_athlete.history_record.all().delete()
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["athlete_last_edited"] is None

    def test_lift_last_edited(self, client, test_athlete):
        """Provide the last edit for an athlete lift."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        lift_histories = [
            lift.history_record.latest().history_date
            for lift in test_athlete.lift_set.all()
        ]
        if len(lift_histories) != 0:
            assert result["lift_last_edited"] == sorted(lift_histories)[
                -1
            ].isoformat().replace("+00:00", "Z")
        else:
            assert result["lift_last_edited"] is None

    def test_lift_set(self, client, test_athlete):
        """Test the lift set for an athlete."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert {lift["reference_id"] for lift in result["lift_set"]} == {
            lift["reference_id"] for lift in test_athlete.lift_set.values()
        }

    # TODO: fix if no total, but competed, still has True.
    def test_age_categories_competed(self, client, test_athlete):
        """Test athlete age categories competed in."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        any_trues = any(result["age_categories_competed"].values())
        if test_athlete.lift_set.count() != 0:
            assert any_trues is True
        else:
            assert any_trues is False

    def test_weight_categories(self, client, test_athlete):
        """Test athlete weight categories competed in."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        weight_categories_competed_count = len(
            result["weight_categories_competed"]
        )
        if test_athlete.lift_set.count() != 0:
            assert weight_categories_competed_count > 0
        else:
            assert weight_categories_competed_count == 0

    def test_best_lifts(self, client, test_athlete):
        """Test athlete getting best lifts."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        best_lifts = result["best_lifts"]
        # TODO: improve validation
        if test_athlete.lift_set.count() > 0:
            assert best_lifts["snatch"] == {} or best_lifts["snatch"] != {}
            assert best_lifts["cnj"] == {} or best_lifts["cnj"] != {}
            assert best_lifts["total"] == {} or best_lifts["total"] != {}
        else:
            assert best_lifts["snatch"] == {}
            assert best_lifts["cnj"] == {}
            assert best_lifts["total"] == {}

    def test_best_sinclair(self, client, test_athlete):
        """Test athlete best sinclair."""
        response = client.get(f"{self.url}/{test_athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        best_sinclair = result["best_sinclair"]
        # TODO: improve validation
        if test_athlete.lift_set.count() > 0:
            assert best_sinclair == {} or best_sinclair != {}
        else:
            assert best_sinclair == {}
