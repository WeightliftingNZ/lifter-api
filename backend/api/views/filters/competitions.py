"""Competition custom filtering."""

from django_filters import rest_framework as filters

from api.models import Competition


class CompetitionFilter(filters.FilterSet):
    """FilterSet class for competition."""

    search = filters.CharFilter(method="search_filter", label="Search")
    date_start = filters.DateFromToRangeFilter(label="Date Range")
    year = filters.NumberFilter(method="year_filter", label="Year")
    ordering = filters.OrderingFilter(fields=(("date_start", "date"),))

    def search_filter(self, queryset, name, value):
        """Search filter method."""
        return Competition.objects.search(query=value)

    def year_filter(self, queryset, name, value):
        """Year filter method."""
        return Competition.objects.year(query=int(value))

    class Meta:
        """Setting for FilterSet class."""

        model = Competition
        fields = ["date_start", "search", "ordering"]
