"""Athlete custom filtering."""

from django.db.models import Q
from django_filters import rest_framework as filters

from api.models import Athlete


class AthleteFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter", label="Search")

    ordering = filters.OrderingFilter(
        fields=(("first_name", "first_name"), ("last_name", "last_name"))
    )

    def search_filter(self, queryset, name, value):
        terms = value.split(" ")

        # prevents overloading search

        if len(terms) > 10:
            terms = terms[:10]
        return queryset.filter(
            *[
                Q(first_name__icontains=term) | (Q(last_name__icontains=term))
                for term in terms
            ]
        )

    class Meta:
        model = Athlete
        fields = ["search", "ordering"]
