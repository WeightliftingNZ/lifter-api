from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Athlete, Competition, Lift


class AthleteAdmin(admin.ModelAdmin):
    readonly_fields = ("reference_id",)
    list_display = ("first_name", "last_name", "yearborn")


class CompetitionAdmin(admin.ModelAdmin):
    readonly_fields = ("reference_id",)
    list_display = ("date_start", "date_end", "location", "competition_name")


class LiftAdmin(admin.ModelAdmin):
    readonly_fields = ("reference_id",)
    fieldsets = (
        (
            None,
            {
                _("fields"): (
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


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Lift, LiftAdmin)
