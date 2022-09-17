"""Athlete custom filtering."""

from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import Q
from django_filters import rest_framework as filters

from api.models import Athlete


class AthleteFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")

    ordering = filters.OrderingFilter(
        fields=(("first_name", "first_name"), ("last_name", "last_name"))
    )

    def search_filter(self, queryset, name, value):
        vector = SearchVector("first_name", "last_name")
        query = SearchQuery(value)
        rank = SearchRank(vector, query)

        return (
            queryset.annotate(search=vector, rank=rank)
            .filter(
                Q(search=query)
                | Q(first_name__trigram_similar=value)
                | Q(last_name__trigram_similar=value)
            )
            .order_by("-rank")
        )

    class Meta:
        model = Athlete
        fields = ["search", "ordering"]
