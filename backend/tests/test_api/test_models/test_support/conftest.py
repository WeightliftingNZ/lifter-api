"""Setting up fixtures for support models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

import pytest

from api.models import (
    AgeCategory,
    AgeCategoryEra,
    WeightCategory,
    WeightCategoryEra,
)


@dataclass
class EraMock:
    """Dataclass to help mock Era objects."""

    date_start: datetime
    description: str | None = None


@dataclass
class AgeCategoryMock:
    """Dataclass to help mock AgeCategory objects."""

    name: str
    era: AgeCategoryEra | None = None
    upper_age_bound: int | None = None
    lower_age_bound: int | None = 0


@dataclass
class WeightCategoryMock:
    """Dataclass to help mock WeightCategory objects."""

    era: WeightCategoryEra
    age_categories: list[AgeCategory]
    sex: Literal["M", "W"]
    weight: int
    is_plus: bool | None = False


@pytest.fixture
def mock_age_category_era(django_db_blocker) -> list[AgeCategoryEra]:
    """Create age category era.

    Returns:
        list[Era]: list of Eras.
    """
    eras = [
        EraMock(
            date_start=datetime(1980, 1, 1),
            description="Age Categories - Current",
        ),
        EraMock(
            date_start=datetime(1960, 1, 1),
            description="Setting another date",
        ),
    ]
    created = []
    for era in eras:
        with django_db_blocker.unblock():
            created.append(
                AgeCategoryEra.objects.create(
                    date_start=era.date_start,
                    description=era.description,
                )
            )
    return created


@pytest.fixture
def mock_age_categories(django_db_blocker) -> list[AgeCategory]:
    """Create Age categories."""
    age_categories = [
        AgeCategoryMock(name="Youth", lower_age_bound=13, upper_age_bound=17),
        AgeCategoryMock(name="Junior", lower_age_bound=15, upper_age_bound=20),
        AgeCategoryMock(name="Senior", lower_age_bound=15),
        AgeCategoryMock(name="Masters", lower_age_bound=35),
        AgeCategoryMock(
            name="Masters 35-39", lower_age_bound=35, upper_age_bound=39
        ),
        AgeCategoryMock(
            name="Masters 40-44", lower_age_bound=40, upper_age_bound=44
        ),
        AgeCategoryMock(
            name="Masters 45-49", lower_age_bound=45, upper_age_bound=49
        ),
        AgeCategoryMock(
            name="Masters 50-54", lower_age_bound=50, upper_age_bound=54
        ),
        AgeCategoryMock(
            name="Masters 54-59", lower_age_bound=55, upper_age_bound=59
        ),
        AgeCategoryMock(
            name="Masters 60-64", lower_age_bound=60, upper_age_bound=64
        ),
        AgeCategoryMock(
            name="Masters 65-69", lower_age_bound=65, upper_age_bound=69
        ),
        AgeCategoryMock(name="Masters 70+", lower_age_bound=70),
    ]
    created = []
    for age_category in age_categories:
        with django_db_blocker.unblock():
            created.append(
                AgeCategory.objects.create(
                    name=age_category.name,
                    upper_age_bound=age_category.upper_age_bound,
                    lower_age_bound=age_category.lower_age_bound,
                )
            )
    return created


@pytest.fixture
def mock_weight_category_era(django_db_blocker) -> list[WeightCategoryEra]:
    """Create Weight category eras."""
    eras = [
        EraMock(
            date_start=datetime(1998, 1, 1),
            description="Weightclasses 1998 - 2017",
        ),
        EraMock(
            date_start=datetime(2017, 1, 1), description="Addition of W90+"
        ),
        EraMock(
            date_start=datetime(2018, 1, 1),
            description="Current weightclasses",
        ),
    ]
    created = []
    for era in eras:
        with django_db_blocker.unblock():
            created.append(
                WeightCategoryEra.objects.create(
                    date_start=era.date_start,
                    description=era.description,
                )
            )
    return created


@pytest.fixture
def mock_weight_categories(
    django_db_blocker,
    mock_weight_category_era,
    mock_age_categories,
) -> list[WeightCategory]:
    """Create weight categories."""
    weight_categories = [
        WeightCategoryMock(
            era=mock_weight_category_era[0],  # 1998-2017,
            age_categories=mock_age_categories[:1],  # Youth only
            sex="W",
            weight=44,
        ),
        WeightCategoryMock(
            era=mock_weight_category_era[0],  # 1998-2017,
            age_categories=mock_age_categories,  # All age categories
            sex="W",
            weight=48,
        ),
        WeightCategoryMock(
            era=mock_weight_category_era[0],  # 1998-2017,
            age_categories=mock_age_categories[1:],  # Not Youth
            sex="W",
            weight=75,
            is_plus=True,
        ),
        WeightCategoryMock(
            era=mock_weight_category_era[2],  # 2018-,
            age_categories=mock_age_categories[:1],  # Youth only
            sex="W",
            weight=40,
        ),
        WeightCategoryMock(
            era=mock_weight_category_era[2],  # 2018-,
            age_categories=mock_age_categories,  # All age categories
            sex="W",
            weight=45,
        ),
        WeightCategoryMock(
            era=mock_weight_category_era[2],  # 2018-,
            age_categories=mock_age_categories[1:],  # Not Youth
            sex="W",
            weight=87,
            is_plus=True,
        ),
    ]
    created = []
    for weight_category in weight_categories:
        with django_db_blocker.unblock():
            wc = WeightCategory.objects.create(
                era=weight_category.era,
                sex=weight_category.sex,
                weight=weight_category.weight,
                is_plus=weight_category.is_plus,
            )
            wc.age_categories.set(weight_category.age_categories)
            created.append(wc)
    return created
