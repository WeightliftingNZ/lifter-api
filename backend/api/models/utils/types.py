"""Custom types."""
from typing import TypedDict

# custom types


class LiftT(TypedDict):
    lift_status: str
    weight: int


class LiftPlacing(TypedDict):
    total_lifted: int
    best_cnj_weight: tuple[str, int]
    lottery_number: int


class AgeCategories(TypedDict):
    is_youth: bool
    is_junior: bool
    is_senior: bool
    is_master: bool
