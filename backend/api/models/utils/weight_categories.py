"""Weight Categories.

Weight categories are imposed at certain 'eras'. A check is performed to \
        ensure the correct weight category is applied to that particular date \
        for the competition.

There is some leeway provided. For example in 2018, weight categories from \
        different eras were accepted as this represented the adoption of new \
        weight categories.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeightCategoryList:
    """Represent the collection of weight categories and the era it was \
            imposed."""

    era_start: datetime
    weight_categories: list[str]


weight_categories_2018 = WeightCategoryList(
    era_start=datetime(2018, 1, 1),
    weight_categories=[
        "W40",
        "W45",
        "W49",
        "W55",
        "W59",
        "W64",
        "W71",
        "W76",
        "W81",
        "W87",
        "W81+",
        "W87+",
        "M49",
        "M55",
        "M61",
        "M67",
        "M73",
        "M81",
        "M89",
        "M96",
        "M102",
        "M109",
        "M102+",
        "M109+",
    ],
)

weight_categories_2017 = WeightCategoryList(
    era_start=datetime(2017, 1, 1),
    weight_categories=[
        "W44",
        "W48",
        "W53",
        "W58",
        "W63",
        "W69",
        "W75",
        "W75+",
        "W90",
        "W90+",
        "M50",
        "M56",
        "M62",
        "M69",
        "M77",
        "M85",
        "M94",
        "M94+",
        "M105",
        "M105+",
    ],
)

weight_categories_1998 = WeightCategoryList(
    era_start=datetime(1998, 1, 1),
    weight_categories=[
        "W44",
        "W48",
        "W53",
        "W58",
        "W63",
        "W69",
        "W75",
        "W75+",
        "M50",
        "M56",
        "M62",
        "M69",
        "M77",
        "M85",
        "M94",
        "M94+",
        "M105",
        "M105+",
    ],
)

weight_category_lists = [
    weight_categories_2018,
    weight_categories_2017,
    weight_categories_1998,
]


def valid_weight_category(weight_category: str, date: datetime) -> bool:
    """Validate weight category for a given date."""
    # order from earlier era to current
    weight_category_lists.sort(key=lambda x: x.era_start)
    for idx, weight_category_list in enumerate(weight_category_lists):
        # check of earliest era
        if (
            idx == 0
            and date <= weight_category_list.era_start
            and weight_category in weight_category_list.weight_categories
        ):
            return True
        if (
            date >= weight_category_list.era_start
            and date <= weight_category_lists[idx + 1].era_start
            and weight_category in weight_category_list.weight_categories
        ):
            return True

        # check current era
        if (
            idx == len(weight_category_lists) - 1
            and date >= weight_category_list.era_start
            and weight_category in weight_category_list.weight_categories
        ):
            return True
    return False
