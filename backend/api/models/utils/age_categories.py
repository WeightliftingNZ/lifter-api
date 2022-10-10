"""Age Categories.

These are the age categories applied. There is an era system applied just in \
        case in the future there are any changes to age categories.
"""

from dataclasses import dataclass
from datetime import datetime


class AgeError(Exception):
    """Error with age."""

    def __init__(self, value, message):
        """Init method."""
        super().__init__(value, message)


@dataclass
class AgeCategory:
    """Particular age category."""

    name: str
    minimum_age: int
    maximum_age: int | None = None

    def __post__init__(self):
        """Validate input."""
        if self.maximum_age and self.minimum_age > self.maximum_age:
            raise AgeError(
                value=[self.maximum_age, self.minimum_age],
                message="maximum_age must be greater than or equal to minimum_age",
            )


@dataclass
class AgeCategoryList:
    """Represent the collection of age categories and the era it was imposed.

    How this will work is that there are a list of categories with a \
            `era_start`. If the list is ordered, the list with the most \
            recent `era_start` will represent the most current, while also \
            that particular `era_start` will act as the end for the previous \
            era.
    """

    era_start: datetime
    age_categories: list[AgeCategory]


age_categories_1990 = AgeCategoryList(
    era_start=datetime(1990, 1, 1),
    age_categories=[
        AgeCategory("Youth", 13, 17),
        AgeCategory("Junior", 15, 20),
        AgeCategory("Senior", 15),
        AgeCategory("Masters", 35),
    ],
)

age_categories = [age_categories_1990]
