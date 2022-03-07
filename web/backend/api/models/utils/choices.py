# TODO include old weight categories
# TODO change labels to e.g Mens' 81kg

__W45 = "W45"
__W49 = "W49"
__W55 = "W55"
__W59 = "W59"
__W64 = "W64"
__W71 = "W71"
__W76 = "W76"
__W81 = "W81"
__W81p = "W81+"

__NEW_FEMALE_WEIGHT_CATEGORIES = [
    (__W45, "W45"),
    (__W49, "W49"),
    (__W55, "W55"),
    (__W59, "W59"),
    (__W64, "W64"),
    (__W71, "W71"),
    (__W76, "W76"),
    (__W81, "W81"),
    (__W81p, "W81+"),
]

__M55 = "M55"
__M61 = "M61"
__M67 = "M67"
__M73 = "M73"
__M81 = "M81"
__M89 = "M89"
__M96 = "M96"
__M102 = "M102"
__M102p = "M102+"

__NEW_MALE_WEIGHT_CATEGORIES = [
    (__M55, "M55"),
    (__M61, "M61"),
    (__M67, "M67"),
    (__M73, "M73"),
    (__M81, "M81"),
    (__M89, "M89"),
    (__M96, "M96"),
    (__M102, "M102"),
    (__M102p, "M102+"),
]

WEIGHT_CATEGORIES = (
    __NEW_MALE_WEIGHT_CATEGORIES + __NEW_FEMALE_WEIGHT_CATEGORIES
)


__LIFT = "LIFT"
__NOLIFT = "NOLIFT"
__NOATTEMPT = "DNA"

LIFT_STATUS = [
    (__LIFT, "Good Lift"),
    (__NOLIFT, "No Lift"),
    (__NOATTEMPT, "Did not attempt"),
]
