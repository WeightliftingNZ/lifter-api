"""Test lift endpoints.

Lift retrieve, create, edit and delete.
"""
from contextlib import nullcontext as does_not_raise

import pytest
from django.core.exceptions import ValidationError
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLift:
    """Lift testing."""

    url = "/v1/competitions"

    def test_retrieve(self, client, lift):
        """Retrieve a lift and include testing payload."""
        response = client.get(
            f"{self.url}/{str(lift.competition.reference_id)}/lifts/{str(lift.reference_id)}"
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["reference_id"] == lift.reference_id
        assert result["url"].split("/")[-1] == lift.reference_id
        assert result["lottery_number"] == lift.lottery_number
        assert result["athlete"] == lift.athlete.reference_id
        assert result["athlete_name"] == lift.athlete.full_name
        assert result["athlete_yearborn"] == lift.athlete.yearborn
        assert result["competition"] == lift.competition.reference_id
        assert result["competition_name"] == lift.competition.name
        assert (
            result["competition_date_start"]
            == str(lift.competition.date_start)[:10]
        )
        assert result["snatch_first"] == lift.snatch_first
        assert result["snatch_first_weight"] == lift.snatch_first_weight
        assert result["snatch_second"] == lift.snatch_second
        assert result["snatch_second_weight"] == lift.snatch_second_weight
        assert result["snatch_third"] == lift.snatch_third
        assert result["snatch_third_weight"] == lift.snatch_third_weight
        assert result["cnj_first"] == lift.cnj_first
        assert result["cnj_first_weight"] == lift.cnj_first_weight
        assert result["cnj_second"] == lift.cnj_second
        assert result["cnj_second_weight"] == lift.cnj_second_weight
        assert result["cnj_third"] == lift.cnj_third
        assert result["cnj_third_weight"] == lift.cnj_third_weight
        assert result["best_snatch_weight"][0] == lift.best_snatch_weight[0]
        assert result["best_snatch_weight"][1] == lift.best_snatch_weight[1]
        assert result["best_cnj_weight"][0] == lift.best_cnj_weight[0]
        assert result["best_cnj_weight"][1] == lift.best_cnj_weight[1]
        assert result["snatches"] == lift.snatches
        assert result["cnjs"] == lift.cnjs
        assert result["total_lifted"] == lift.total_lifted
        assert result["sinclair"] == float(lift.sinclair)
        assert result["grade"] == lift.grade
        assert result["age_categories"] == lift.age_categories
        assert str(result["bodyweight"]) == str(lift.bodyweight)
        assert result["weight_category"] == lift.weight_category
        assert result["team"] == lift.team
        assert result["session_number"] == lift.session_number
        assert result["placing"] == lift.placing

    def test_list(self, client, mock_lift):
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
    def test_admin_create(
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
                    # comp in in 2022
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
            # FIXME: disabled Weight class validation
            # pytest.param(
            #     {
            #         "snatch_first": "LIFT",
            #         "snatch_first_weight": 101,
            #         "snatch_second": "LIFT",
            #         "snatch_second_weight": 101,
            #         "snatch_third": "LIFT",
            #         "snatch_third_weight": 102,
            #         "cnj_first": "NOLIFT",
            #         "cnj_first_weight": 100,
            #         "cnj_second": "LIFT",
            #         "cnj_second_weight": 99,
            #         "cnj_third": "DNA",
            #         "cnj_third_weight": 0,
            #         "bodyweight": 102.00,
            #         "weight_category": "M105+",
            #         "team": "TEST",
            #         "session_number": 0,
            #         "lottery_number": 3,
            #     },
            #     pytest.raises(
            #         ValidationError,
            #         match=r"Weightclass from wrong era.",
            #     ),
            #     id="Weightclass from wrong era.",
            # ),
        ],
    )
    def test_create_validation(
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
        "test_input_lift_1,test_input_lift_2,status_code,error_message",
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
                status.HTTP_201_CREATED,
                None,
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
                status.HTTP_400_BAD_REQUEST,
                {"Only one lottery number per weight category"},
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
                status.HTTP_400_BAD_REQUEST,
                {"Only one lottery number per weight category"},
                id="Same lottery number for a weight category",
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
                status.HTTP_201_CREATED,
                None,
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
                status.HTTP_201_CREATED,
                None,
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
                status.HTTP_400_BAD_REQUEST,
                {
                    "Athlete can only have one lift in a competition",
                    "Only one lottery number per weight category",
                },
                id="Athlete twice in same competition.",
            ),
        ],
    )
    def test_create_constraints(
        self,
        admin_client,
        mock_athlete,
        mock_competition,
        test_input_lift_1,
        test_input_lift_2,
        status_code,
        error_message,
    ):
        """Test builtin constraints on Lift model.

        1. `lottery_number` and `weight_category` must be unique for every
        competition (i.e. a no two lifts can have the same `lottery_number`
        and `weight_category`).
        2. An athlete cannot be entered more than once into a competition.
        """
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
        assert response_1.status_code == status.HTTP_201_CREATED
        assert response_2.status_code == status_code

        if response_2.status_code == status.HTTP_400_BAD_REQUEST:
            assert error_message == set(response_2.json()["non_field_errors"])

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
        "test_input,status_code,error_message",
        [
            pytest.param(
                {
                    "reference_id": 0,
                    "lottery_number": 4,
                },
                status.HTTP_200_OK,
                None,
                id="Normal edit",
            ),
            pytest.param(
                {
                    "reference_id": 0,
                    "lottery_number": 2,
                },
                status.HTTP_400_BAD_REQUEST,
                {"Only one lottery number per weight category"},
                id="Edit same lottery number in same competition",
            ),
            pytest.param(
                {
                    "reference_id": 2,
                    "lottery_number": 2,
                },
                status.HTTP_200_OK,
                None,
                id="Edit same lottery number but different competitions",
            ),
            pytest.param(
                {
                    "reference_id": 1,
                    "lottery_number": 3,
                    "athlete": 0,
                },
                status.HTTP_400_BAD_REQUEST,
                {"Athlete can only have one lift in a competition"},
                id="Edit athlete duplicated competition.",
            ),
            pytest.param(
                {
                    "reference_id": 2,
                    "competition": 0,
                },
                status.HTTP_400_BAD_REQUEST,
                {
                    "Only one lottery number per weight category",
                    "Athlete can only have one lift in a competition",
                },
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
        status_code,
        error_message,
    ):
        """Test builtin constraints on edit.

        1. `lottery_number` and `weight_category` must remain unique for each
        competition.
        2. An athlete can not have more than one lift per competition.
        """
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
        assert response.status_code == status_code

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            assert error_message == set(response.json()["non_field_errors"])

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
