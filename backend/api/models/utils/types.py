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
    is_master_35_39: bool
    is_master_40_44: bool
    is_master_45_49: bool
    is_master_50_54: bool
    is_master_55_59: bool
    is_master_60_64: bool
    is_master_65_69: bool
    is_master_70: bool
