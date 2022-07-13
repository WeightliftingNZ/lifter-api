"""Contains helper functions for the models."""
from datetime import datetime


def ranking_suffixer(rank: int) -> str:
    """Provide ordering ranking e.g. 1st, 11th, 21st.

    Args:
        rank (int): rank or placing.

    Returns:
        str: ordering rank.
    """
    str_rank = str(rank)
    suffix = "th"
    if len(str_rank) > 1:
        if str_rank[-2:] in ["11", "12", "13"]:
            return f"{str_rank}{suffix}"
    if str_rank[-1] == "1":
        suffix = "st"
    elif str_rank[-1] == "2":
        suffix = "nd"
    elif str_rank[-1] == "3":
        suffix = "rd"
    return f"{str_rank}{suffix}"


def best_lift(lifts: dict[str, dict[str, str | int]]) -> tuple[str, int]:
    """Give best lift.

    This will return the lift attempt and the best lift e.g. ("1st", 100)

    If no attempt was made then an empty string and 0 will be returned e.g
    ("", 0)

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


def key_sort_lifts(lift: dict[str, str | int]) -> tuple[int, int, int, int]:
    """Sort key for lifts.

    Args:
        lift (dict[str, str | int]): this contains the lift data

    Returns:
        tuple[int, int, int, int]: the keys to be used in the sorted parameter
    """
    keys = (
        # total
        -lift["total_lifted"],
        # lowest cnj
        lift["best_cnj_weight"][1],
        # least attempts
        lift["best_cnj_weight"][0],
        # lott number
        lift["lottery_number"],
    )
    return keys

def age_category(yearborn, competition_year=None)  -> dict[str, bool]:
    """Give age category.

    From: https://iwf.sport/weightlifting_/participants/
        - YOUTH: 13 – 17 years of age
        - JUNIOR: 15 – 20 years of age
        - SENIOR: ≥15 years of age
        - MASTERS: ≥35 years of age

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
        # TODO: what to do if this happens?
        pass

    return {
            "is_youth": years_from_birth >= 13 and years_from_birth <= 17,
            "is_junior": years_from_birth >= 15 and years_from_birth <= 20,
            "is_senior": years_from_birth >= 15,
            "is_master": years_from_birth >= 35,
            }
