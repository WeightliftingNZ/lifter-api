"""Competition custom filtering."""

from django_filters import rest_framework as filters

from api.models import Competition


class CompetitionFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")
    date_start = filters.DateFromToRangeFilter(label="Date Range")
    ordering = filters.OrderingFilter(fields=(("date_start", "date"),))

    def search_filter(self, queryset, name, value):
        return Competition.objects.search(query=value)

    class Meta:
        model = Competition
        fields = ["date_start", "search", "ordering"]
