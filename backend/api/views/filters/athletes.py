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
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    class Meta:
        model = Athlete
        fields = ["search", "ordering"]
