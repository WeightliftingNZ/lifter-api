from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.contrib import admin

from api.models import AthleteModel, CompetitionModel, SessionModel, LifterModel


class AthleteAdmin(admin.ModelAdmin):
    readonly_fields = ("reference_id",)
    list_display = ("first_name", "last_name", "yearborn")


class CompetitionAdmin(admin.ModelAdmin):
    readonly_fields = ("reference_id",)
    list_display = ("date_start", "date_end", "location", "competition_name")


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ("session_id",)
    list_display = ("date", "competition")


admin.site.register(AthleteModel, AthleteAdmin)
admin.site.register(CompetitionModel, CompetitionAdmin)
admin.site.register(SessionModel, SessionAdmin)
