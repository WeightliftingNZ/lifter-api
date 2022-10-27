"""Admin interface."""

from datetime import datetime

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from .models import Athlete, Competition, Lift


class AthleteAdmin(admin.ModelAdmin):
    """Athlete admin."""

    search_fields = ("first_name", "last_name")
    readonly_fields = (
        "reference_id",
        "full_name",
        "age_categories",
    )
    list_display = ("first_name", "last_name", "yearborn", "view_lifts_link")

    def view_lifts_link(self, obj):
        """Provide link to lifts for a athlete."""
        count = obj.lift_set.count()
        url = (
            reverse("admin:api_lift_changelist")
            + "?"
            + urlencode({"athlete__reference_id": f"{obj.reference_id}"})
        )
        return format_html('<a href="{}">{} Lifts</a>', url, count)


class CompetitionYearListFilter(admin.SimpleListFilter):
    """Filter Competition by year."""

    title = _("Competition Year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """Lookup."""
        qs = model_admin.get_queryset(request)
        return {(q.date_start.year, q.date_start.year) for q in qs}

    def queryset(self, request, queryset):
        """Queryset."""
        if self.value() is not None and self.value().isdigit():
            year = int(self.value())
            return queryset.filter(
                date_start__gte=datetime(year, 1, 1),
                date_start__lte=datetime(year, 12, 31),
            )
        return queryset


class CompetitionAdmin(admin.ModelAdmin):
    """Competition Admin."""

    search_fields = ("name", "location")
    readonly_fields = ("reference_id",)
    list_display = (
        "name",
        "view_lifts_link",
        "date_start",
        "show_date_start_year",
        "location",
    )
    list_filter = (CompetitionYearListFilter,)

    def view_lifts_link(self, obj):
        """Provide link to lifts for a competition."""
        count = obj.lift_set.count()
        url = (
            reverse("admin:api_lift_changelist")
            + "?"
            + urlencode({"competition__reference_id": f"{obj.reference_id}"})
        )
        return format_html('<a href="{}">{} Lifts</a>', url, count)

    def show_date_start_year(self, obj):
        """Provide the year of the competition."""
        return obj.date_start.year


class LiftCompetitionYearListFilter(admin.SimpleListFilter):
    """Filter Competition by year for lift models."""

    title = _("Year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        """Lookup."""
        qs = model_admin.get_queryset(request)
        return {
            (q.competition.date_start.year, q.competition.date_start.year)
            for q in qs
        }

    def queryset(self, request, queryset):
        """Queryset."""
        if self.value() is not None and self.value().isdigit():
            year = int(self.value())
            return queryset.filter(
                competition__date_start__gte=datetime(year, 1, 1),
                competition__date_start__lte=datetime(year, 12, 31),
            )
        return queryset


class LiftCompetitionNameListFilter(admin.SimpleListFilter):
    """Filter Competition name when a year is selected.

    The aim of this is to reduce the number of names shown. And if no year is \
            selected, then this will not display.
    """

    title = _("Name")
    parameter_name = "competition__reference_id"

    def lookups(self, request, model_admin):
        """Lookup is  the lift's competition name."""
        if (
            request.GET.get("year") is not None
            and request.GET.get("year").isdigit()
        ):
            qs = model_admin.get_queryset(request)
            year = int(request.GET.get("year"))
            qs = qs.filter(
                competition__date_start__gte=datetime(year, 1, 1),
                competition__date_start__lte=datetime(year, 12, 31),
            )
            competitions = {q.competition for q in qs}
            return (
                (competition.reference_id, competition.name)
                for competition in competitions
            )

    def queryset(self, request, queryset):
        """Queryset depends on the competition `reference_id`.

        Prevents duplicates since this is the lift queryset.
        """
        if self.value() is not None:
            return queryset.filter(competition__reference_id=self.value())
        return queryset


class LiftAdmin(admin.ModelAdmin):
    """Lift Admin."""

    search_fields = (
        "competition__name",
        "competition__location",
        "athlete__first_name",
        "athlete__last_name",
    )
    readonly_fields = ("reference_id",)
    list_display = ("athlete", "competition")
    list_filter = (
        LiftCompetitionYearListFilter,
        LiftCompetitionNameListFilter,
    )
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


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Lift, LiftAdmin)
