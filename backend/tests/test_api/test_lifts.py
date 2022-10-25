"""Test lift."""

import json
from contextlib import nullcontext as does_not_raise

import pytest
from django.core import serializers
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models import Athlete, Competition, Lift

pytestmark = pytest.mark.django_db


class BaseTestLift:
    """Base Test class for Lift testing."""

    url = "/v1/competitions"


class TestLiftModel:
    """Testing Lift model functions.

    Includes:
        - Normal CRUD operations.
        - Validation:
        TODO?
    """

    def test_instance(self, lift):
        """Ensure the created instance is a Lift model instance."""
        assert isinstance(lift, Lift)

    def test_all(self, batch_lift):
        """Can retrieve entire Lift table."""
        lift_table = Lift.objects.all()
        assert {lift.reference_id for lift in batch_lift} == {
            lift.reference_id for lift in lift_table
        }

    def test_get(self, lift, batch_lift):
        """Can retrieve a single lift."""
        retrieved_lift = Lift.objects.filter(reference_id=lift.reference_id)
        assert retrieved_lift.exists() is True
        assert retrieved_lift.first().reference_id not in [
            lift.reference_id for lift in batch_lift
        ]

    # TODO: write edge cases!
    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(0, does_not_raise(), id="normal"),
        ],
    )
    def test_create(
        self, lift_factory, competition, athlete, test_input, exception
    ):
        """Able to create a lift."""
        with exception:
            lift_stub = lift_factory.stub().__dict__
            lift_stub["athlete"] = athlete
            lift_stub["competition"] = competition
            lift = Lift.objects.create(
                **lift_stub,
            )
            assert (
                Lift.objects.filter(reference_id=lift.reference_id).exists()
                is True
            )

    @pytest.mark.parametrize(
        "test_input,exception",
        [pytest.param(0, does_not_raise(), id="normal")],
    )
    def test_update(
        self, lift, competition, athlete, lift_factory, test_input, exception
    ):
        """Able to create a lift."""
        updated_lift = Lift.objects.get(reference_id=lift.reference_id)
        new_details = lift_factory.stub().__dict__
        new_details["athlete"] = athlete
        new_details["competition"] = competition
        for attr, value in new_details.items():
            setattr(updated_lift, attr, value)
        with exception:
            updated_lift.save()
            assert json.loads(serializers.serialize("json", [updated_lift]))[
                0
            ].get("fields") != json.loads(
                serializers.serialize("json", [lift])
            )[
                0
            ].get(
                "fields"
            )

    def test_delete(self, lift):
        """Test lift deletion.

        In the future, this will be a soft delete.
        """
        Lift.objects.get(reference_id=lift.reference_id).delete()
        assert (
            Lift.objects.filter(reference_id=lift.reference_id).exists()
            is False
        )

    def test_custom_properties(self, lift):
        """Testing the custom model properties of the `Lift` model."""
        custom_properties = [
            "snatches",
            "cnjs",
            "best_cnj_weight",
            "best_snatch_weight",
            "total_lifted",
            "age_categories",
            "sinclair",
            "placing",
            "grade",
        ]
        assert all(
            [
                getattr(lift, custom_property)
                for custom_property in custom_properties
            ]
        )


class TestLiftManager:
    """Lift custom manager functionality tests."""

    def test_ordered_filter(self, competition_with_lifts_weight_categories):
        """Test ordered filter functionality."""
        (
            competition,
            weight_category_original,
        ) = competition_with_lifts_weight_categories
        lifts = Lift.objects.ordered_filter(competition=competition)
        lifts_weight_category = [lift.weight_category for lift in lifts]
        assert lifts_weight_category == weight_category_original

    def test_search_empty_query(self, batch_lift):
        """Test for search manager function when `query=None`."""
        search_result = Lift.objects.search(query=None)
        assert Lift.objects.all().count() == len(batch_lift)
        assert search_result.count() == Lift.objects.all().count()

    @pytest.mark.parametrize(
        "test_inputs",
        [
            pytest.param(
                (("athlete", "first_name"),), id="athlete-first-name"
            ),
            pytest.param((("athlete", "last_name"),), id="athlete-last-name"),
            pytest.param((("athlete", "full_name"),), id="athlete-full-name"),
        ],
    )
    def test_search(self, lift, batch_lift, test_inputs):
        """Test search functionality."""
        query = []
        for test_input in test_inputs:
            model, field = test_input
            query.append(getattr(getattr(lift, model), field))
        search_result = Lift.objects.search(query=" ".join(query))
        assert Lift.objects.all().count() == len(batch_lift) + 1
        assert search_result.count() < len(batch_lift) + 1
        assert lift.reference_id in {
            result.reference_id for result in search_result
        }


class TestLiftEndpoints(BaseTestLift):
    """Test functionality of lift endpoints.

    This includes commonly accessed (not authenticated required):
        - listing lifts from a competition
        - retrieving a lift

    as well as  higher privileges:
        - creating a lift
        - editing a lift
        - deleting a lift

    Higher privileged actions require administration level, but in the future \
            this will be moved to a group.
    """

    def test_list(self, client, competition_with_lifts):
        """List competition lifts."""
        response = client.get(
            f"{self.url}/{str(competition_with_lifts.reference_id)}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert (
            result["lifts_count"]
            == Lift.objects.filter(competition=competition_with_lifts).count()
        )

    def test_retrieve(self, client, lift):
        """Retrieve a lift and include testing payload."""
        response = client.get(
            f"{self.url}/{lift.competition.reference_id}/lifts/{lift.reference_id}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        serialized_lift = json.loads(serializers.serialize("json", [lift]))[
            0
        ].get("fields")
        common_keys = set(result.keys() & serialized_lift.keys())
        assert (
            all([result[k] == serialized_lift[k] for k in common_keys]) is True
        )

    @pytest.mark.parametrize(
        "test_client,expected",
        [
            pytest.param(
                lazy_fixture("client"), status.HTTP_401_UNAUTHORIZED, id="anon"
            ),
            pytest.param(
                lazy_fixture("admin_client"),
                status.HTTP_201_CREATED,
                id="admin",
            ),
        ],
    )
    def test_create(
        self, test_client, expected, lift_factory, competition, athlete
    ):
        """Lifts can be created by an admin user and not anon user."""
        lift = lift_factory.stub().__dict__
        lift["competition"] = str(competition.reference_id)
        lift["athlete"] = str(athlete.reference_id)
        response = test_client.post(
            f"{self.url}/{str(competition.reference_id)}/lifts",
            data=lift,
            content_type="application/json",
        )
        assert response.status_code == expected
        lift_exists = Lift.objects.filter(
            reference_id=response.json().get("reference_id")
        ).exists()
        if response.status_code == status.HTTP_201_CREATED:
            assert lift_exists is True
        else:
            assert lift_exists is False

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
        self, test_client, expected, lift, lift_factory, competition, athlete
    ):
        """Admin users can edit lifts but not anon user."""
        edited_lift = lift_factory.stub().__dict__
        edited_lift["competition"] = str(
            Competition.objects.create(
                **edited_lift["competition"].__dict__
            ).reference_id
        )
        edited_lift["athlete"] = str(
            Athlete.objects.create(
                **edited_lift["athlete"].__dict__
            ).reference_id
        )
        response = test_client.patch(
            f"{self.url}/{lift.competition.reference_id}/lifts/{lift.reference_id}",
            data=edited_lift,
            content_type="application/json",
        )
        assert response.status_code == expected
        result = response.json()
        current_lift = json.loads(
            serializers.serialize(
                "json", [Lift.objects.get(reference_id=lift.reference_id)]
            )
        )[0].get("fields")
        previous_lift = json.loads(serializers.serialize("json", [lift]))[
            0
        ].get("fields")

        if response.status_code == status.HTTP_200_OK:
            assert current_lift != previous_lift
            common_keys = set(
                result.keys() & current_lift.keys() & previous_lift.keys()
            )
            assert (
                all([result[k] == previous_lift[k] for k in common_keys])
                is False
            )
            assert (
                all([result[k] == current_lift[k] for k in common_keys])
                is True
            )
        else:
            assert current_lift == previous_lift

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
    def test_delete(self, test_client, expected, lift):
        """Lift can be deleted by an admin user and not anon user."""
        response = test_client.delete(
            f"{self.url}/{lift.competition.reference_id}/lifts/{lift.reference_id}"
        )
        assert response.status_code == expected
        lift_exists = Lift.objects.filter(
            reference_id=lift.reference_id
        ).exists()
        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert lift_exists is False
        else:
            assert lift_exists is True
