"""Test lift endpoints.

Lift retrieve, create, edit and delete.
"""
from contextlib import nullcontext as does_not_raise

import pytest
from django.core.exceptions import ValidationError
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLiftCase:
    """Lift testing."""

    url = "/v1/competitions"

    def test_get_lifts(self, client, mock_lift):
        """Retrieve lifts for a competition."""
        response = client.get(
            f"{self.url}/{str(mock_lift[0].competition.reference_id)}/lifts"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] >= 1
        mock_lift_ids = [lift.reference_id for lift in mock_lift]
        result_lift_ids = [lift["reference_id"] for lift in result["results"]]
        assert set(mock_lift_ids) == set(result_lift_ids)

    def test_get_lift(self, client, mock_lift):
        """Retrieve a specific lift using a id."""
        IDX = 0
        response = client.get(
            f"{self.url}/{str(mock_lift[IDX].competition.reference_id)}/lifts/{mock_lift[IDX].reference_id}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["team"] == mock_lift[IDX].team

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 3,
                },
                status.HTTP_201_CREATED,
                id="Normal input.",
            ),
            pytest.param(
                {
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "WRONG",
                    "session_number": 0,
                    "team": "TEST",
                    "lottery_number": 3,
                },
                status.HTTP_400_BAD_REQUEST,
                id="`weight_category` incorrect.",
            ),
        ],
    )
    def test_admin_create_lift(
        self,
        admin_client,
        mock_athlete,
        mock_competition,
        test_input,
        expected,
    ):
        """Admin users can create lifts."""
        test_input["competition"] = str(mock_competition[0].reference_id)
        test_input["athlete"] = str(mock_athlete[0].reference_id)
        response = admin_client.post(
            f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                does_not_raise(),
                id="Normal input",
            ),
            pytest.param(
                {
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 101,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 3,
                },
                pytest.raises(
                    ValidationError,
                    match="2nd snatch cannot be lower or same than previous lift if a good lift.",
                ),
                id="2nd snatch not incremented",
            ),
        ],
    )
    def test_create_lift_custom_validation(
        self,
        admin_client,
        mock_athlete,
        mock_competition,
        test_input,
        expected,
    ):
        """Test custom validation of lift model."""
        with expected:
            test_input["competition"] = str(mock_competition[0].reference_id)
            test_input["athlete"] = str(mock_athlete[0].reference_id)
            response = admin_client.post(
                f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
                data=test_input,
                content_type="application/json",
            )
            assert response is not None

    @pytest.mark.parametrize(
        "test_input_lift_1,test_input_lift_2,expected",
        [
            pytest.param(
                {
                    "competition": 0,
                    "athlete": 0,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                {
                    "competition": 0,
                    "athlete": 1,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 2,
                },
                does_not_raise(),
                id="Normal input",
            ),
            pytest.param(
                {
                    "competition": 0,
                    "athlete": 0,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                {
                    "competition": 0,
                    "athlete": 1,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                pytest.raises(
                    ValidationError,
                    match="Cannot have the same lottery number in a session.",
                ),
                id="Same lottery number in same competition",
            ),
            pytest.param(
                {
                    "competition": 0,
                    "athlete": 0,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                {
                    "competition": 1,
                    "athlete": 0,
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 100,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "LIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 101,
                    "cnj_third": "LIFT",
                    "cnj_third_weight": 102,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 1,
                },
                does_not_raise(),
                id="Same lottery number in different competitions",
            ),
        ],
    )
    def test_create_lift_lottery_number(
        self,
        admin_client,
        mock_athlete,
        mock_competition,
        test_input_lift_1,
        test_input_lift_2,
        expected,
    ):
        """Lottery Numbers cannot be the same for the same session."""
        with expected:
            test_input_lift_1["competition"] = str(
                mock_competition[test_input_lift_1["competition"]].reference_id
            )
            test_input_lift_1["athlete"] = str(
                mock_athlete[test_input_lift_1["athlete"]].reference_id
            )
            test_input_lift_2["competition"] = str(
                mock_competition[test_input_lift_2["competition"]].reference_id
            )
            test_input_lift_2["athlete"] = str(
                mock_athlete[test_input_lift_2["athlete"]].reference_id
            )
            response_1 = admin_client.post(
                f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
                data=test_input_lift_1,
                content_type="application/json",
            )
            response_2 = admin_client.post(
                f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
                data=test_input_lift_2,
                content_type="application/json",
            )
            assert response_1 is not None
            assert response_2 is not None

    def test_anon_create_lift(
        self,
        client,
        mock_athlete,
        mock_competition,
    ):
        """Anonymous users cannot create lifts."""
        data = {}
        data["competition"] = str(mock_competition[0].reference_id)
        data["athlete"] = str(mock_athlete[0].reference_id)
        response = client.post(
            f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
            data=data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "bodyweight": 103.00,
                },
                status.HTTP_200_OK,
                id="Normal edit",
            ),
            pytest.param(
                {
                    "bodyweight": "ThisIsNotANumber",
                },
                status.HTTP_400_BAD_REQUEST,
                id="`bodyweight` incorrect",
            ),
        ],
    )
    def test_admin_edit_lift(
        self, admin_client, mock_lift, test_input, expected
    ):
        """Admin users can edit lifts."""
        response = admin_client.patch(
            f"{self.url}/{str(mock_lift[0].competition.reference_id)}/lifts/{str(mock_lift[0].reference_id)}",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "lift": 1,
                    "lottery_number": 4,
                },
                does_not_raise(),
                id="Normal edit",
            ),
            pytest.param(
                {
                    "lift": 1,
                    "lottery_number": 1,
                },
                pytest.raises(ValidationError, match=""),
                id="Edit same lottery number in same competition",
            ),
            pytest.param(
                {
                    "lift": 2,
                    "lottery_number": 1,
                },
                does_not_raise(),
                id="Edit same lottery number but different competitions",
            ),
        ],
    )
    def test_edit_lift_lottery_number(
        self, admin_client, mock_lift, test_input, expected
    ):
        """Edit lottery numbers."""
        with expected:
            idx = test_input["lift"]
            test_input.pop("lift")
            response = admin_client.patch(
                f"{self.url}/{str(mock_lift[idx].competition.reference_id)}/lifts/{str(mock_lift[idx].reference_id)}",
                data=test_input,
                content_type="application/json",
            )
            assert response is not None

    def test_anon_edit_lift(self, client, mock_lift):
        """Anonymous users cannot edit lifts."""
        response = client.patch(
            f"{self.url}/{str(mock_lift[0].competition.reference_id)}/lifts/{str(mock_lift[0].reference_id)}",
            data={},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_delete_lift(
        self,
        admin_client,
        mock_lift,
    ):
        """Admin users can delete lifts."""
        response = admin_client.delete(
            f"{self.url}/{str(mock_lift[0].competition.reference_id)}/lifts/{str(mock_lift[0].reference_id)}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_anon_delete_lift(self, client, mock_lift):
        """Anonymous users cannot delete lifts."""
        response = client.delete(
            f"{self.url}/{str(mock_lift[0].competition.reference_id)}/lifts/{str(mock_lift[0].reference_id)}",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
