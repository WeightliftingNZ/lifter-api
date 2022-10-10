"""Testing athlete endpoints."""

from contextlib import nullcontext as does_not_raise
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models import Athlete, Lift
from api.models.utils.constants import GRADES
from config.settings import MINIMUM_YEAR_FROM_BIRTH

pytestmark = pytest.mark.django_db


class BaseTestAthlete:
    """Base Test Class for Athlete testing."""

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
        """Can retrieve entire table."""
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
                id="model-create-age-validation-old-enough",
            ),
            pytest.param(
                datetime.now().year - (MINIMUM_YEAR_FROM_BIRTH - 1),
                pytest.raises(
                    ValidationError,
                    match=r".*yearborn.*",
                ),
                id="model-create-age-validation-too-young",
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
                id="model-update-age-validation-old-enough",
            ),
            pytest.param(
                datetime.now().year - (MINIMUM_YEAR_FROM_BIRTH - 1),
                pytest.raises(
                    ValidationError,
                    match=r".*yearborn.*",
                ),
                id="model-update-age-validation-too-young",
            ),
        ],
    )
    def test_update(self, athlete, athlete_factory, test_input, exception):
        """Able to update athlete."""
        with exception:
            updated_athlete = Athlete.objects.get(
                reference_id=athlete.reference_id
            )
            new_details = athlete_factory.stub(yearborn=test_input).__dict__
            for attr, value in new_details.items():
                setattr(updated_athlete, attr, value)
            updated_athlete.save()
            assert updated_athlete.first_name != athlete.first_name
            assert updated_athlete.last_name != athlete.last_name
            assert updated_athlete.yearborn != athlete.yearborn

    def test_delete(self, athlete):
        """Test athlete deletion. In the future this will be made into a soft \
                delete."""
        Athlete.objects.get(reference_id=athlete.reference_id).delete()
        assert (
            Athlete.objects.filter(reference_id=athlete.reference_id).exists()
            is False
        )

    def test_age_categories(self, athlete):
        """Testing age_categories property."""
        assert (
            Athlete.objects.get(
                reference_id=athlete.reference_id
            ).age_categories
            == athlete.age_categories
        )

    def test_full_name(self, athlete):
        """Testing full name combination from `first_name` and `last_name`."""
        assert (
            Athlete.objects.get(reference_id=athlete.reference_id).full_name
            == f"{athlete.first_name.title()} {athlete.last_name.title()}"
        )


class TestAthleteManager:
    """Athlete custom manager functionality tests."""

    def test_search_query_full_name(self, athlete, batch_athlete):
        """Testing search query on the athlete's full name."""
        search_result = Athlete.objects.search(query=athlete.full_name)
        assert Athlete.objects.all().count() == len(batch_athlete) + 1
        assert search_result.count() < len(batch_athlete) + 1
        assert search_result.first().reference_id == athlete.reference_id

    def test_search_query_none(self, batch_athlete):
        """Test for search manager function when `query=None`."""
        search_result = Athlete.objects.search(query=None)
        assert Athlete.objects.all().count() == len(batch_athlete)
        assert search_result.count() == Athlete.objects.all().count()


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
        """List athletes.

        Batch creates athletes one more than the `PAGE_SIZE`. Since the batch \
        size is greater than the pagination, the results should paginate.

        Test will check if all the generated athletes are present but the \
        last one, since this paginated to the next page.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == len(batch_athlete)

    def test_retrieve(self, client, athlete):
        """Retrieve athlete."""
        response = client.get(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["first_name"] == athlete.first_name

    def test_filter_no_query(self, client, athlete):
        """Blank search query gives no results."""
        response = client.get(f"{self.url}?search=''")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == 0
        # check athlete exists
        assert isinstance(athlete, Athlete)

    @pytest.mark.parametrize("athlete__first_name", ["John"])
    @pytest.mark.parametrize("athlete__last_name", ["Doe"])
    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param("John", id="athlete-filter-first-name"),
            pytest.param("Doe", id="athlete-filter-last-name"),
            pytest.param("John Doe", id="athlete-filter-full-name"),
        ],
    )
    def test_filter_with_inputs(self, client, athlete, test_input):
        """List and retrieve athlete by filter."""
        response = client.get(f"{self.url}?search={test_input}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] > 0
        assert result["results"][0]["first_name"] == athlete.first_name

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
    def test_create(self, test_client, expected, athlete_factory):
        """Athlete can only be created by an admin user and not anon user."""
        athlete = athlete_factory.stub()
        response = test_client.post(
            self.url,
            data=athlete.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected

        # check creation
        count = Athlete.objects.filter(
            reference_id=response.json().get("reference_id")
        ).count()
        if response.status_code == status.HTTP_201_CREATED:
            assert count == 1
        else:
            assert count == 0

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="athlete-edit-anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_200_OK,
                id="athlete-edit-admin",
            ),
        ],
    )
    def test_edit(self, test_client, expected, athlete, athlete_factory):
        """Admin users can edit athletes but not anon users."""
        edited_athlete = athlete_factory.stub()
        response = test_client.patch(
            f"{self.url}/{athlete.reference_id}",
            data=edited_athlete.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected

        # check editing
        extract_athlete = Athlete.objects.get(
            reference_id=athlete.reference_id
        )
        if response.status_code == status.HTTP_200_OK:
            assert extract_athlete.first_name == edited_athlete.first_name
            assert extract_athlete.last_name == edited_athlete.last_name
            assert extract_athlete.yearborn == edited_athlete.yearborn
        else:
            assert extract_athlete.first_name != edited_athlete.first_name
            assert extract_athlete.last_name != edited_athlete.last_name
            assert extract_athlete.yearborn != edited_athlete.yearborn

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"),
                status.HTTP_401_UNAUTHORIZED,
                id="athlete-edit-anon",
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_204_NO_CONTENT,
                id="athlete-edit-admin",
            ),
        ],
    )
    def test_delete(self, test_client, expected, athlete):
        """Admin users can delete athletes, but not anon users."""
        response = test_client.delete(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == expected

        # check deletion
        count = Athlete.objects.filter(
            reference_id=athlete.reference_id
        ).count()
        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert count == 0
        else:
            assert count == 1


class TestAthleteSerializer(BaseTestAthlete):
    """Testing the Athlete Serializer custom fields."""

    def test_lift_counts(self, client, athlete_with_lifts):
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
            id="athlete-with-lifts",
        ),
        pytest.param(lazy_fixture("athlete"), id="athlete-no-lifts"),
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
        if test_athlete.lift_set.count() != 0:
            assert best_lifts["total"] != {}
        if test_athlete.lift_set.count() == 0:
            assert best_lifts["snatch"] == {}
            assert best_lifts["cnj"] == {}
            assert best_lifts["total"] == {}
