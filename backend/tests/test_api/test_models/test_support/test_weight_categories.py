"""Testing Weight Categorey models methods and validation."""


import pytest

# from api.models import AgeCategory, AgeCategoryEra
from api.models import WeightCategory, WeightCategoryEra

pytestmark = pytest.mark.django_db


class TestWeightCategoryEra:
    @pytest.mark.xfail(
        reason="need to rewrite this test, not critical at the moment"
    )
    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param(0, id="WC_era_1998_2017"),
            pytest.param(1, id="WC_era_2017_2018"),
            pytest.param(2, id="WC_era_2018_current"),
        ],
    )
    def test_str_representation(self, mock_weight_category_era, test_input):
        """String representation of the model."""
        era = mock_weight_category_era[test_input]
        era_from_models = WeightCategoryEra.objects.get(
            reference_id=era.reference_id
        )
        date_start = era_from_models.date_start
        date_end = era_from_models.date_end
        if date_end is None:
            assert (
                str(era) == f"Weight Category Era: {date_start.year} - Current"
            )
        else:
            assert (
                str(era)
                == f"Weight Category Era: {date_start.year} - {date_end.year}"
            )


class TestWeightCategory:
    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param(0, id="1998_W44"),
        ],
    )
    def test_str_representation(self, mock_weight_categories, test_input):
        """String representation of the model."""
        weight_category = mock_weight_categories[test_input]
        weight_category_from_models = WeightCategory.objects.get(
            reference_id=weight_category.reference_id
        )
        sex = weight_category_from_models.sex
        weight = weight_category_from_models.weight
        is_plus = weight_category_from_models.is_plus
        assert str(weight_category) == f"{sex}{weight}{'+' if is_plus else ''}"

    # @pytest.mark.parametrize(
    #     "test_input,exception",
    #     [
    #         pytest.param(
    #             AgeCategoryMock(
    #                 name="Youth", upper_age_bound=17, lower_age_bound=13
    #             ),
    #             does_not_raise(),
    #             id="age_cat_youth",
    #         ),
    #         pytest.param(
    #             AgeCategoryMock(name="Master 70+", lower_age_bound=70),
    #             does_not_raise(),
    #             id="age_cat_70+",
    #         ),
    #         pytest.param(
    #             AgeCategoryMock(
    #                 name="Wrong1", upper_age_bound=13, lower_age_bound=17
    #             ),
    #             pytest.raises(
    #                 ValidationError,
    #                 match=r"upper_age_bound must be larger than lower_age_bound.",
    #             ),
    #             id="err_age_cat_upper_lt_lower",
    #         ),
    #         pytest.param(
    #             AgeCategoryMock(
    #                 name="Wrong1", upper_age_bound=13, lower_age_bound=-17
    #             ),
    #             pytest.raises(
    #                 ValidationError,
    #                 match=r"lower_age_bound must be positive.",
    #             ),
    #             id="err_age_cat_lower_neg",
    #         ),
    #         pytest.param(
    #             AgeCategoryMock(
    #                 name="Wrong2", upper_age_bound=-1, lower_age_bound=17
    #             ),
    #             pytest.raises(
    #                 ValidationError,
    #                 match=r"['upper_age_bound must be positive.', 'upper_age_bound must be larger than lower_age_bound']",
    #             ),
    #             id="err_age_cat_upper_neg_upper_lt_lower",
    #         ),
    #     ],
    # )
    # def test_custom_validation(self, test_input, exception):
    #     """Test the custom validation."""
    #     with exception:
    #         age_category = AgeCategory.objects.create(
    #             name=test_input.name,
    #             upper_age_bound=test_input.upper_age_bound,
    #             lower_age_bound=test_input.lower_age_bound,
    #         )
    #         assert age_category.name == test_input.name
