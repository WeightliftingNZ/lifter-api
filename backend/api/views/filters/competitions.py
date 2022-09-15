"""Competition custom filtering."""

from django.db.models import Q
from django_filters import rest_framework as filters

from api.models import Competition


class CompetitionFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")
    date_start = filters.DateFromToRangeFilter(label="Date Range")

    ordering = filters.OrderingFilter(fields=(("date_start", "date"),))

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(location__icontains=value)
        )

    class Meta:
        model = Competition
        fields = ["date_start", "search", "ordering"]
