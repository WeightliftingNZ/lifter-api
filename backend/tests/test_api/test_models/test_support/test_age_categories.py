"""Testing Age Categories model methods and validation."""

from contextlib import nullcontext as does_not_raise

import pytest
from django.core.exceptions import ValidationError

from api.models import AgeCategory, AgeCategoryEra

from .conftest import AgeCategoryMock

pytestmark = pytest.mark.django_db


class TestAgeCategoryEra:
    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param(0, id="Normal 1970"),
            pytest.param(1, id="Normal 1960"),
        ],
    )
    def test_str_representation(self, mock_age_category_era, test_input):
        """String representation of the model."""
        era = mock_age_category_era[test_input]
        era_from_models = AgeCategoryEra.objects.get(
            reference_id=era.reference_id
        )
        date_start = era_from_models.date_start
        date_end = era_from_models.date_end
        if date_end is None:
            assert str(era) == f"Age Category Era: {date_start.year} - Current"
        else:
            assert (
                str(era)
                == f"Age Category Era: {date_start.year} - {date_end.year}"
            )


class TestAgeCategory:
    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param(0, id="Youth"),
            pytest.param(1, id="Junior"),
            pytest.param(2, id="Senior"),
            pytest.param(3, id="Masters"),
            pytest.param(4, id="Masters 35-39"),
            pytest.param(5, id="Masters 40-44"),
            pytest.param(6, id="Masters 45-49"),
            pytest.param(7, id="Masters 50-54"),
            pytest.param(8, id="Masters 55-59"),
            pytest.param(9, id="Masters 60-64"),
            pytest.param(10, id="Masters 65-69"),
            pytest.param(11, id="Masters 70+"),
        ],
    )
    def test_str_representation(self, mock_age_categories, test_input):
        """String representation of the model."""
        age_category = mock_age_categories[test_input]
        age_category_from_models = AgeCategory.objects.get(
            reference_id=age_category.reference_id
        )
        name = age_category.name
        upper_age_bound = age_category_from_models.upper_age_bound
        lower_age_bound = age_category_from_models.lower_age_bound
        if upper_age_bound is None:
            assert str(age_category) == f"{name}: {lower_age_bound} <= age"
        else:
            assert (
                str(age_category)
                == f"{name}: {lower_age_bound} <= age <= {upper_age_bound}"
            )

    @pytest.mark.parametrize(
        "test_input,exception",
        [
            pytest.param(
                AgeCategoryMock(
                    name="Youth", upper_age_bound=17, lower_age_bound=13
                ),
                does_not_raise(),
                id="age_cat_youth",
            ),
            pytest.param(
                AgeCategoryMock(name="Master 70+", lower_age_bound=70),
                does_not_raise(),
                id="age_cat_70+",
            ),
            pytest.param(
                AgeCategoryMock(
                    name="Wrong1", upper_age_bound=13, lower_age_bound=17
                ),
                pytest.raises(
                    ValidationError,
                    match=r"upper_age_bound must be larger than lower_age_bound.",
                ),
                id="err_age_cat_upper_lt_lower",
            ),
            pytest.param(
                AgeCategoryMock(
                    name="Wrong1", upper_age_bound=13, lower_age_bound=-17
                ),
                pytest.raises(
                    ValidationError,
                    match=r"lower_age_bound must be positive.",
                ),
                id="err_age_cat_lower_neg",
            ),
            pytest.param(
                AgeCategoryMock(
                    name="Wrong2", upper_age_bound=-1, lower_age_bound=17
                ),
                pytest.raises(
                    ValidationError,
                    match=r"['upper_age_bound must be positive.', 'upper_age_bound must be larger than lower_age_bound']",
                ),
                id="err_age_cat_upper_neg_upper_lt_lower",
            ),
        ],
    )
    def test_custom_validation(self, test_input, exception):
        """Test the custom validation."""
        with exception:
            age_category = AgeCategory.objects.create(
                name=test_input.name,
                upper_age_bound=test_input.upper_age_bound,
                lower_age_bound=test_input.lower_age_bound,
            )
            assert age_category.name == test_input.name
