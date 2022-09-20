"""Contains helper functions for the models."""
import math
from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError

from .types import AgeCategories, LiftT


def ranking_suffixer(rank: int) -> str:
    """Provide ordering ranking e.g. 1st, 11th, 21st.

    Args:
        rank (int): rank or placing.

    Returns:
        str: ordering rank.
    """
    str_rank = str(rank)
    suffix = "th"
    if len(str_rank) > 1 and str_rank[-2:] in ["11", "12", "13"]:
        return f"{str_rank}{suffix}"
    if str_rank[-1] == "1":
        suffix = "st"
    elif str_rank[-1] == "2":
        suffix = "nd"
    elif str_rank[-1] == "3":
        suffix = "rd"
    return f"{str_rank}{suffix}"


def best_lift(lifts: dict[str, LiftT]) -> tuple[str, int]:
    """Give best lift.

        This will return the lift attempt and the best lift e.g. ("1st", 100).

        If no attempt was made then an empty string and 0 will be returned e.g
        ("", 0).

    Args:
        lifts (LiftPlacing): this contains the lift data

    Returns:
        tuple[str, int]: The best lift attempt and the best lift weight.
    """
    parsed_lifts = [
        (lift_key, lift_value["lift_status"], lift_value["weight"])
        for lift_key, lift_value in lifts.items()
    ]
    best_lift = 0
    best_lift_attempt = ""
    for lift_attempt, lift_made, lift_weight in parsed_lifts:
        if lift_made == "LIFT" and lift_weight > best_lift:
            best_lift = lift_weight
            best_lift_attempt = lift_attempt
    return best_lift_attempt, best_lift


def validate_attempts(attempts: dict[str, LiftT], lift_type: str):
    """Validate attempts.

    If an attempt is a good lift, then the next attempt has to be an
    incremented.

    If an attempt is not made, then the next attempt has to be an same or
    more.

    Args:
        attempts (dict[str, LiftT]): Attempts.
        lift_type (str): Must be either "snatch" or "clean and jerk".
    """
    if lift_type not in ["snatch", "clean and jerk"]:
        raise Exception("lift_type must be 'snatch' or 'clean and jerk'")
    PLACING = {0: "1st", 1: "2nd", 2: "3rd"}
    lst_attempts = list(attempts.values())
    # loop through attempts and check the next attempt
    errors = []
    for i, attempt in enumerate(lst_attempts):
        # ignore last attempt and DNA future attempts
        if (
            i < len(lst_attempts) - 1
            and lst_attempts[i + 1]["lift_status"] != "DNA"
        ):
            # if the next attempt is a GOOD lift, the current attempt
            # should be less than, so throw error if next attempt is
            # less than or equal than current
            if (
                attempt["lift_status"] == "LIFT"
                and attempt["weight"] >= lst_attempts[i + 1]["weight"]
            ):

                errors.append(
                    f"{PLACING[i]} {lift_type} is a GOOD lift. Next attempt cannot be lower or same than previous lift."
                )

            # if the next attempt is a NO lift, the current attempt
            # should be less than or same, so throw error if
            # next attempt is less than current
            if (
                attempt["lift_status"] == "NOLIFT"
                and attempt["weight"] > lst_attempts[i + 1]["weight"]
            ):
                errors.append(
                    f"{PLACING[i]} {lift_type} is a NO lift. Next attempt cannot be less than previous lift."
                )
        return errors


def age_category(yearborn: int, competition_year: int = None) -> AgeCategories:
    """Give age category.

    From: https://iwf.sport/weightlifting_/participants/
        - YOUTH: 13 – 17 years of age
        - JUNIOR: 15 – 20 years of age
        - SENIOR: ≥15 years of age
        - MASTERS: ≥35 years of age

        Further categories for masters:
            - 35 - 39
            - 40 - 44
            - 44 - 49
            - 50 - 54
            - 55 - 59
            - 60 - 64
            - 65 - 69
            - 70+

    Args:
        yearborn: The year the athlete was born.
        competition_year: The year when the competition took place.
        Default is None. If not supplied, then it is set to current year.

    Returns:
        dict[str, bool]: Validations.
    """
    if competition_year is None:
        competition_year = datetime.now().year

    years_from_birth = competition_year - yearborn

    if years_from_birth < 0:
        raise ValidationError(
            "Age of athlete is negative: %(years_from_birth)s",
            code="yearborn error",
            params={
                "years_from_birth": years_from_birth,
            },
        )

    return {
        "is_youth": years_from_birth >= 13 and years_from_birth <= 17,
        "is_junior": years_from_birth >= 15 and years_from_birth <= 20,
        "is_senior": years_from_birth >= 15,
        "is_master": years_from_birth >= 35,
        "is_master_35_39": years_from_birth >= 35 and years_from_birth <= 39,
        "is_master_40_44": years_from_birth >= 40 and years_from_birth <= 44,
        "is_master_45_49": years_from_birth >= 45 and years_from_birth <= 49,
        "is_master_50_54": years_from_birth >= 50 and years_from_birth <= 54,
        "is_master_55_59": years_from_birth >= 55 and years_from_birth <= 59,
        "is_master_60_64": years_from_birth >= 60 and years_from_birth <= 64,
        "is_master_65_69": years_from_birth >= 65 and years_from_birth <= 39,
        "is_master_70": years_from_birth >= 70,
    }


def calculate_sinclair(
    bodyweight: Decimal,
    total_lifted: int,
    weight_category: str,
    yearborn: int,
    lift_year: int,
) -> Decimal:
    """Calculate the sinclair for a lift.

    Args:
        bodyweight (Decimal):  Bodyweight of athlete for particular lift.
        total_lifted (int): Total lifted for lift.
        weight_category (str): Athlete's weight category for particular lift.
        yearborn (int): Athlete's birth year.
        lift_year (int): The year the lift took place (competition).

    Returns:
        Decimal: Sinclair rounded to 3 decimal places.
    """
    SINCLAIR_CONSTANTS = {
        "M": {"a": Decimal(0.751945030), "b": Decimal(175.508)},
        "W": {"a": Decimal(0.783497476), "b": Decimal(153.655)},
    }

    AGE_CORRECTION = Decimal(1)

    # TODO:
    # sinclair change at every olympic cycle
    # also age adjusted?
    if yearborn:
        pass

    if lift_year:
        pass

    sex = weight_category[0]
    a = SINCLAIR_CONSTANTS[sex]["a"]
    b = SINCLAIR_CONSTANTS[sex]["b"]

    if bodyweight <= b:
        x = Decimal(math.log10(Decimal(bodyweight) / b))
        ax2 = x**2 * a
        sinclair_coefficient = Decimal(10) ** ax2
    else:
        sinclair_coefficient = Decimal(1)

    sinclair_total = total_lifted * sinclair_coefficient * AGE_CORRECTION
    return round(sinclair_total, 3)
