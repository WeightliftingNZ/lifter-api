"""Contains current and old weightclasses."""

from django.utils.translation import gettext_lazy as _

# 2018-Present

__W40 = "W40"  # Youth only class
__W45 = "W45"
__W49 = "W49"
__W55 = "W55"
__W59 = "W59"
__W64 = "W64"
__W71 = "W71"
__W76 = "W76"
__W81 = "W81"
__W87 = "W87"  # Senior/Junior only class
__W81p = "W81+"  # Youth only class
__W87p = "W87+"  # Senior/Junior only class

CURRENT_YOUTH_ONLY_FEMALE_WEIGHT_CATEGORIES = [
    (__W40, "W40"),
    (__W81p, "W81+"),
]

CURRENT_SENIOR_JUNIOR_ONLY_FEMALE_WEIGHT_CATEGORIES = [
    (__W87, "W87"),
    (__W87p, "W87+"),
]


CURRENT_FEMALE_WEIGHT_CATEGORIES = (
    [
        (__W45, "W45"),
        (__W49, "W49"),
        (__W55, "W55"),
        (__W59, "W59"),
        (__W64, "W64"),
        (__W71, "W71"),
        (__W76, "W76"),
        (__W81, "W81"),
    ]
    + CURRENT_YOUTH_ONLY_FEMALE_WEIGHT_CATEGORIES
    + CURRENT_SENIOR_JUNIOR_ONLY_FEMALE_WEIGHT_CATEGORIES
)

__M49 = "M49"  # Youth only class
__M55 = "M55"
__M61 = "M61"
__M67 = "M67"
__M73 = "M73"
__M81 = "M81"
__M89 = "M89"
__M96 = "M96"
__M102 = "M102"
__M109 = "M109"  # Senior/Junior only class
__M102p = "M102+"  # Youth only class
__M109p = "M109+"  # Senior/Junior only class

CURRENT_YOUTH_ONLY_MALE_WEIGHT_CATEGORIES = [
    (__M49, "M49"),  # Youth only class
    (__M102p, "M102+"),  # Youth only class
]

CURRENT_SENIOR_JUNIOR_ONLY_MALE_WEIGHT_CATEGORIES = [
    (__M109, "M109"),  # Senior/Junior only class
    (__M109p, "M109+"),  # Senior/Junior only class
]

CURRENT_MALE_WEIGHT_CATEGORIES = (
    [
        (__M55, "M55"),
        (__M61, "M61"),
        (__M67, "M67"),
        (__M73, "M73"),
        (__M81, "M81"),
        (__M89, "M89"),
        (__M96, "M96"),
        (__M102, "M102"),
    ]
    + CURRENT_YOUTH_ONLY_MALE_WEIGHT_CATEGORIES
    + CURRENT_SENIOR_JUNIOR_ONLY_MALE_WEIGHT_CATEGORIES
)

# TODO: separate Youth/Senior/Junior classes.

# 1998-2018

__W44 = "W44"  # Youth
__W48 = "W48"
__W53 = "W53"
__W58 = "W58"
__W63 = "W63"
__W69 = "W69"
__W75 = "W75"
__W75p = "W75+"  # Youth
__W90 = "W90"  # Senior/Junior
__W90p = "W90+"  # Senior/Junior

OLD_1998_2018_FEMALE_WEIGHT_CATEGORIES = [
    (__W44, "W44"),  # Youth
    (__W48, "W48"),
    (__W53, "W53"),
    (__W58, "W58"),
    (__W63, "W63"),
    (__W69, "W69"),
    (__W75, "W75"),
    (__W75p, "W75+"),  # Youth
    (__W90, "W90"),
    (__W90p, "W90+"),
]

__M50 = "M50"  # Youth
__M56 = "M56"
__M62 = "M62"
__M69 = "M69"
__M77 = "M77"
__M85 = "M85"
__M94 = "M94"
__M94p = "M94+"  # Youth
__M105 = "M105"  # Senior
__M105p = "M105+"  # Senior

OLD_1998_2018_MALE_WEIGHT_CATEGORIES = [
    (__M50, "M50"),
    (__M56, "M56"),
    (__M62, "M62"),
    (__M69, "M69"),
    (__M77, "M77"),
    (__M85, "M85"),
    (__M94, "M94"),
    (__M94p, "M94+"),
    (__M105, "M105"),
    (__M105p, "M105+"),
]


WEIGHT_CATEGORIES = (
    CURRENT_FEMALE_WEIGHT_CATEGORIES
    + CURRENT_MALE_WEIGHT_CATEGORIES
    + OLD_1998_2018_FEMALE_WEIGHT_CATEGORIES
    + OLD_1998_2018_MALE_WEIGHT_CATEGORIES
)


__LIFT = "LIFT"
__NOLIFT = "NOLIFT"
__NOATTEMPT = "DNA"

DEFAULT_LIFT_STATUS = __NOATTEMPT

LIFT_STATUS = [
    (__LIFT, "Good Lift"),
    (__NOLIFT, "No Lift"),
    (__NOATTEMPT, "Did not attempt"),
]

__YOUTH = "YTH"
__JUNIOR = "JNR"
__SENIOR = "SNR"
__MASTERS_35_39 = "MS35"
__MASTERS_40_49 = "MS40"
__MASTERS_50_54 = "MS50"
__MASTERS_55_59 = "MS55"
__MASTERS_60_64 = "MS60"
__MASTERS_65_69 = "MS65"
__MASTERS_70p = "MS70"

AGE_CATEGORIES = [
    (__YOUTH, _("Youth")),
    (__JUNIOR, _("Junior")),
    (__SENIOR, _("Senior")),
    (__MASTERS_35_39, _("Master 35-39")),
    (__MASTERS_40_49, _("Master 40-49")),
    (__MASTERS_50_54, _("Master 50-54")),
    (__MASTERS_55_59, _("Master 55-59")),
    (__MASTERS_60_64, _("Master 60-64")),
    (__MASTERS_65_69, _("Master 65-69")),
    (__MASTERS_70p, _("Master 70+")),
]
