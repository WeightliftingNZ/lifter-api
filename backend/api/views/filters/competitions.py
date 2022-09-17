"""Competition custom filtering."""

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import Q
from django_filters import rest_framework as filters

from api.models import Competition


class CompetitionFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")
    date_start = filters.DateFromToRangeFilter(label="Date Range")
    ordering = filters.OrderingFilter(fields=(("date_start", "date"),))

    def search_filter(self, queryset, name, value):
        vector = SearchVector("name", "location")
        query = SearchQuery(value)
        rank = SearchRank(vector, query)

        return (
            queryset.annotate(search=vector, rank=rank)
            .filter(
                Q(search=query)
                | Q(name__trigram_similar=value)
                | Q(location__trigram_similar=value)
            )
            .order_by("-rank")
        )

    class Meta:
        model = Competition
        fields = ["date_start", "search", "ordering"]
