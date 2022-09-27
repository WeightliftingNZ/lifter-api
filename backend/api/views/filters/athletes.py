"""Athlete custom filtering."""

from django_filters import rest_framework as filters

from api.models import Athlete


class AthleteFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")

    ordering = filters.OrderingFilter(
        fields=(("first_name", "first_name"), ("last_name", "last_name"))
    )

    def search_filter(self, queryset, name, value):
        return Athlete.objects.search(query=value)

    class Meta:
        model = Athlete
        fields = ["search", "ordering"]
