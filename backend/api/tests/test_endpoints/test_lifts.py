"""Test lift endpoints.

Lift retrieve, create, edit and delete.
"""
from contextlib import nullcontext as does_not_raise
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLiftCase:
    """Lift testing."""

    url = "/v1/competitions"

    def test_get_lifts(self, client, mock_lift):
        """Retrieve lifts for a competition."""
        competition_id = mock_lift[0].competition.reference_id
        response = client.get(f"{self.url}/{str(competition_id)}/lifts")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) >= 1
        mock_lift_ids = [
            lift.reference_id
            for lift in mock_lift
            if lift.competition.reference_id == competition_id
        ]
        result_lift_ids = [lift["reference_id"] for lift in result]
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
                    match=r"1st snatch is a GOOD lift. Next attempt cannot be lower or same than previous lift.",
                ),
                id="2nd snatch not incremented",
            ),
            pytest.param(
                {
                    "snatch_first": "LIFT",
                    "snatch_first_weight": 101,
                    "snatch_second": "LIFT",
                    "snatch_second_weight": 101,
                    "snatch_third": "LIFT",
                    "snatch_third_weight": 102,
                    "cnj_first": "NOLIFT",
                    "cnj_first_weight": 100,
                    "cnj_second": "LIFT",
                    "cnj_second_weight": 99,
                    "cnj_third": "DNA",
                    "cnj_third_weight": 0,
                    "bodyweight": 102.00,
                    "weight_category": "M102+",
                    "team": "TEST",
                    "session_number": 0,
                    "lottery_number": 3,
                },
                pytest.raises(
                    ValidationError,
                    match=r"1st snatch is a GOOD lift. Next attempt cannot be lower or same than previous lift.\\n1st clean and jerk is a NO lift. Next attempt cannot be less than previous lift.",
                ),
                id="Multiple attempts do not increment",
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
                    match="Lift with this Competition, Lottery number and Weight category already exists.",
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
                    "session_number": 1,
                    "lottery_number": 1,
                },
                pytest.raises(
                    ValidationError,
                    match="Lift with this Competition and Athlete already exists.",
                ),
                id="Athlete twice in same competition.",
            ),
        ],
    )
    def test_create_lift_constraints(
        self,
        admin_client,
        mock_athlete,
        mock_competition,
        test_input_lift_1,
        test_input_lift_2,
        expected,
    ):
        """Test builtin constraints on Lift model.

        1. `lottery_number` and `session_numbers` must be unique for every
        competition (i.e. a no two lifts can have the same `lottery_number`
        and `session_number`.
        2. An athlete cannot be entered more than once into a competition.
        """
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
        data = {
            "competition": str(mock_competition[0].reference_id),
            "athlete": str(mock_athlete[0].reference_id),
        }
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
        IDX = 0
        response = admin_client.patch(
            f"{self.url}/{str(mock_lift[IDX].competition.reference_id)}/lifts/{str(mock_lift[IDX].reference_id)}",
            data=test_input,
            content_type="application/json",
        )
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "reference_id": 0,
                    "lottery_number": 4,
                },
                does_not_raise(),
                id="Normal edit",
            ),
            pytest.param(
                {
                    "reference_id": 0,
                    "lottery_number": 2,
                },
                pytest.raises(
                    ValidationError,
                    match="Lift with this Competition, Lottery number and Weight category already exists.",
                ),
                id="Edit same lottery number in same competition",
            ),
            pytest.param(
                {
                    "reference_id": 2,
                    "lottery_number": 2,
                },
                does_not_raise(),
                id="Edit same lottery number but different competitions",
            ),
            pytest.param(
                {
                    "reference_id": 1,
                    "lottery_number": 3,
                    "athlete": 0,
                },
                pytest.raises(
                    ValidationError,
                    match="Lift with this Competition and Athlete already exists.",
                ),
                id="Edit athlete duplicated competition.",
            ),
            pytest.param(
                {
                    "reference_id": 2,
                    "competition": 0,
                },
                pytest.raises(
                    ValidationError,
                    match="['Lift with this Competition, Lottery number and Session number already exists.', 'Lift with this Competition and Athlete already exists.']",
                ),
                id="Edit athlete already exists.",
            ),
        ],
    )
    def test_edit_lift_constraints(
        self,
        admin_client,
        mock_lift,
        mock_athlete,
        mock_competition,
        test_input,
        expected,
    ):
        """Test builtin constraints on edit.

        1. `lottery_number` and `session_number` must remain unique for each
        competition.
        2. An athlete can not have more than one lift per competition.
        """
        with expected:
            if test_input.get("competition") is not None:
                test_input["competition"] = str(
                    mock_competition[test_input["competition"]].reference_id
                )
            if test_input.get("athlete") is not None:
                test_input["athlete"] = str(
                    mock_athlete[test_input["athlete"]].reference_id
                )
            idx = test_input["reference_id"]
            test_input.pop("reference_id")
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

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {
                    "athlete": {
                        "first_name": "One",
                        "last_name": "Athlete-One",
                        "yearborn": datetime.now().year - 21,
                    },
                    "lift": {
                        "snatch_first": "LIFT",
                        "snatch_first_weight": 100,
                        "snatch_second": "NOLIFT",
                        "snatch_second_weight": 110,
                        "snatch_third": "DNA",
                        "snatch_third_weight": 0,
                        "cnj_first": "NOLIFT",
                        "cnj_first_weight": 140,
                        "cnj_second": "LIFT",
                        "cnj_second_weight": 140,
                        "cnj_third": "LIFT",
                        "cnj_third_weight": 145,
                        "bodyweight": 101.00,
                        "weight_category": "M102+",
                        "team": "TEST",
                        "session_number": 1,
                        "lottery_number": 1,
                    },
                },
                {
                    "snatches": {
                        "1st": {"lift_status": "LIFT", "weight": 100},
                        "2nd": {"lift_status": "NOLIFT", "weight": 110},
                        "3rd": {"lift_status": "DNA", "weight": 0},
                    },
                    "best_snatch_weight": ["1st", 100],
                    "cnjs": {
                        "1st": {"lift_status": "NOLIFT", "weight": 140},
                        "2nd": {"lift_status": "LIFT", "weight": 140},
                        "3rd": {"lift_status": "LIFT", "weight": 145},
                    },
                    "best_cnj_weight": ["3rd", 145],
                    "total_lifted": 245,
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                id="Normal Senior",
            ),
            pytest.param(
                {
                    "athlete": {
                        "first_name": "One",
                        "last_name": "Athlete-One",
                        "yearborn": datetime.now().year - 15,
                    },
                    "lift": {
                        "snatch_first": "LIFT",
                        "snatch_first_weight": 100,
                        "snatch_second": "NOLIFT",
                        "snatch_second_weight": 110,
                        "snatch_third": "DNA",
                        "snatch_third_weight": 0,
                        "cnj_first": "NOLIFT",
                        "cnj_first_weight": 140,
                        "cnj_second": "LIFT",
                        "cnj_second_weight": 140,
                        "cnj_third": "LIFT",
                        "cnj_third_weight": 145,
                        "bodyweight": 101.00,
                        "weight_category": "M102+",
                        "team": "TEST",
                        "session_number": 1,
                        "lottery_number": 1,
                    },
                },
                {
                    "snatches": {
                        "1st": {"lift_status": "LIFT", "weight": 100},
                        "2nd": {"lift_status": "NOLIFT", "weight": 110},
                        "3rd": {"lift_status": "DNA", "weight": 0},
                    },
                    "best_snatch_weight": ["1st", 100],
                    "cnjs": {
                        "1st": {"lift_status": "NOLIFT", "weight": 140},
                        "2nd": {"lift_status": "LIFT", "weight": 140},
                        "3rd": {"lift_status": "LIFT", "weight": 145},
                    },
                    "best_cnj_weight": ["3rd", 145],
                    "total_lifted": 245,
                    "age_categories": {
                        "is_youth": True,
                        "is_junior": True,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                id="Youth, Junior, Senior",
            ),
        ],
    )
    def test_lift_payload_custom_properties(
        self, admin_client, mock_competition, test_input, expected
    ):
        """Test the lift payload of custom properties."""
        athlete_url = "/v1/athletes"
        athlete = admin_client.post(
            athlete_url,
            data=test_input["athlete"],
            content_type="application/json",
        )
        test_input["lift"]["competition"] = str(
            mock_competition[0].reference_id
        )
        test_input["lift"]["athlete"] = athlete.json()["reference_id"]
        response = admin_client.post(
            f"{self.url}/{str(mock_competition[0].reference_id)}/lifts",
            data=test_input["lift"],
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["snatches"] == expected["snatches"]
        assert result["best_snatch_weight"] == expected["best_snatch_weight"]
        assert result["cnjs"] == expected["cnjs"]
        assert result["best_cnj_weight"] == expected["best_cnj_weight"]
        assert result["total_lifted"] == expected["total_lifted"]
        assert result["age_categories"] == expected["age_categories"]
