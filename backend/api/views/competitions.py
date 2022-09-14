"""Viewset for competitions."""

from rest_framework import viewsets

from api.models import Competition
from api.serializers import CompetitionDetailSerializer, CompetitionSerializer
from api.views.pagination import StandardSetPagination

from .filters import CompetitionFilter


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    Competition
    ========
    - List of Competitions on database.
    - Paginated
    """

    filterset_class = CompetitionFilter
    ordering = ["-date_start"]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        return Competition.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CompetitionDetailSerializer
        return CompetitionSerializer
