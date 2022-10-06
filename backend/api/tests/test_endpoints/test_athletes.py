"""Testing athlete endpoints."""

from datetime import datetime

import pytest
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from api.models.athletes import Athlete
from config.settings import MINIMUM_YEAR_FROM_BIRTH

pytestmark = pytest.mark.django_db


class _BaseTestAthlete:
    """Athlete Testing Base class."""

    url = "/v1/athletes"


class TestAthleteCommon(_BaseTestAthlete):
    """Test functionality that requires no authentication (a.k.a. "common").

    This includes:
        - listing many athletes
        - retrieving an athlete
        - searching/filtering on athletes
    """

    def test_list(self, client, mock_athlete):
        """List athletes.

        `mock_athlete` fixture batch creates athletes one more than the \
                `PAGE_SIZE`. Since the batch size is greater than the \
                pagination, the results should paginate.

        Test will check if all the generated athletes are present but the last \
                one, since this paginated to the next page.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["count"] == len(mock_athlete)
        mock_athlete_ids = [
            str(athlete.reference_id) for athlete in mock_athlete
        ]
        mock_athlete_ids_but_last = mock_athlete_ids[:-1]
        page_one_result_athlete_ids = [
            athlete["reference_id"] for athlete in result["results"]
        ]
        assert set(mock_athlete_ids_but_last) == set(
            page_one_result_athlete_ids
        )
        assert mock_athlete_ids[-1] not in page_one_result_athlete_ids

    def test_retrieve(self, client, athlete):
        """Retrieve athlete."""
        response = client.get(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["first_name"] == athlete.first_name
        assert result["last_name"] == athlete.last_name
        assert result["yearborn"] == athlete.yearborn
        # properties
        assert result["age_categories"] == athlete.age_categories
        assert result["full_name"] == athlete.full_name

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


class TestAthleteRescricted(_BaseTestAthlete):
    """Test functionality that requires higher level privileges.

    This includes:
        - creating an athlete
        - editing an athlete
        - deleting an athlete
    which can only be invoked by admin accounts (at the moment). In the \
            this might be enacted by a specific user group.
    """

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
        """Admin users can edit athletes."""
        edited_athlete = athlete_factory.stub()
        response = test_client.patch(
            f"{self.url}/{athlete.reference_id}",
            data=edited_athlete.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected
        extract_athlete = Athlete.objects.get(
            reference_id=athlete.reference_id
        )

        # check editing
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
    def test_admin_delete(self, test_client, expected, athlete):
        """Admin users can delete athletes."""
        response = test_client.delete(f"{self.url}/{athlete.reference_id}")
        assert response.status_code == expected

        # check deletion.

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                datetime.now().year - MINIMUM_YEAR_FROM_BIRTH,
                status.HTTP_201_CREATED,
                id="create-age-validation-old-enough",
            ),
            pytest.param(
                datetime.now().year - (MINIMUM_YEAR_FROM_BIRTH - 1),
                status.HTTP_400_BAD_REQUEST,
                id="create-age-validation-too-young",
            ),
        ],
    )
    def test_admin_create_yearborn_validation(
        self,
        admin_client,
        athlete_factory,
        test_input,
        expected,
    ):
        """Testing Athlete custom validation.

        Athlete must be over the minimum year from birth.
        """
        athlete = athlete_factory.stub(yearborn=test_input)
        response = admin_client.post(
            self.url,
            data=athlete.__dict__,
            content_type="application/json",
        )
        assert response.status_code == expected
        # TODO test the response json


class TestAthleteSpecial(_BaseTestAthlete):
    pass
