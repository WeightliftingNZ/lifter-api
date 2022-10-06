"""Athlete custom filtering."""

from django_filters import rest_framework as filters

from api.models import Athlete


class AthleteFilter(filters.FilterSet):
    """Custom athlete filter."""

    search = filters.CharFilter(method="search_filter", label="Search")

    ordering = filters.OrderingFilter(
        fields=(("first_name", "first_name"), ("last_name", "last_name"))
    )

    def search_filter(self, queryset, name, value):
        """Search filter.

        If an empty query is provided then empty queryset is returned.
        """
        return Athlete.objects.search(query=value)

    class Meta:
        """Setting for the filter."""

        model = Athlete
        fields = ["search", "ordering"]
