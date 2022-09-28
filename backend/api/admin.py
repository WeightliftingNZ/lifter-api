from django.contrib import admin

from .models import (
    AgeCategory,
    AgeCategoryEra,
    Athlete,
    Competition,
    Lift,
    WeightCategory,
    WeightCategoryEra,
)


class AthleteAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")
    readonly_fields = (
        "reference_id",
        "full_name",
        "age_categories",
    )
    list_display = ("first_name", "last_name", "yearborn")


class CompetitionAdmin(admin.ModelAdmin):
    search_fields = ("name", "location")
    readonly_fields = ("reference_id",)
    list_display = ("date_start", "date_end", "location", "name")


class LiftAdmin(admin.ModelAdmin):
    search_fields = (
        "competition__name",
        "competition__location",
        "athlete__first_name",
        "athlete__last_name",
    )
    readonly_fields = ("reference_id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "reference_id",
                    "athlete",
                    "competition",
                )
            },
        ),
        (
            "Lifts",
            {
                "fields": (
                    "snatch_first",
                    "snatch_first_weight",
                    "snatch_second",
                    "snatch_second_weight",
                    "snatch_third",
                    "snatch_third_weight",
                    "cnj_first",
                    "cnj_first_weight",
                    "cnj_second",
                    "cnj_second_weight",
                    "cnj_third",
                    "cnj_third_weight",
                )
            },
        ),
        (
            "Other",
            {
                "fields": (
                    "bodyweight",
                    "weight_category",
                    "team",
                    "lottery_number",
                )
            },
        ),
    )


class AgeCategoryEraAdmin(admin.ModelAdmin):
    """Admin view for AgeCategoryEra model.

    `date_end` and `is_current` are readonly because they are determined by \
            `date_start`, which is editable.
    """

    readonly_fields = ("reference_id", "date_end", "is_current")
    fieldsets = (
        (
            None,
            {"fields": ("date_start", "description")},
        ),
    )


class AgeCategoryAdmin(admin.ModelAdmin):
    """Admin view for AgeCategory model."""

    readonly_fields = ("reference_id",)
    fieldsets = (
        (
            "Relationships",
            {"fields": ("era",)},
        ),
        (
            "Age Category",
            {"fields": ("name", "lower_age_bound", "upper_age_bound")},
        ),
    )


class WeightCategoryEraAdmin(admin.ModelAdmin):
    """Admin view for WeightCategoryEra model.

    `date_end` and `is_current` are readonly because they are determined by \
            `date_start`, which is editable.
    """

    readonly_fields = ("reference_id", "date_end", "is_current")
    fieldsets = (
        (
            None,
            {"fields": ("date_start", "description")},
        ),
    )


class WeightCategoryAdmin(admin.ModelAdmin):
    """Admin view for AgeCategory model."""

    readonly_fields = ("reference_id",)
    fieldsets = (
        (
            "Relationships",
            {"fields": ("era", "age_categories")},
        ),
        (
            "Weight Category",
            {"fields": ("sex", "weight", "is_plus")},
        ),
    )


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Lift, LiftAdmin)
admin.site.register(AgeCategoryEra, AgeCategoryEraAdmin)
admin.site.register(AgeCategory, AgeCategoryAdmin)
admin.site.register(WeightCategoryEra, WeightCategoryEraAdmin)
admin.site.register(WeightCategory, WeightCategoryAdmin)
