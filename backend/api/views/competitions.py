from rest_framework import filters, viewsets

from api.models import Competition
from api.serializers import CompetitionDetailSerializer, CompetitionSerializer
from api.views.pagination import StandardSetPagination


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    Competiition
    ========
    - List of Competitions on database.
    - Paginated
    """

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "location"]
    ordering_fields = ["date_start"]
    ordering = ["-date_start"]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        return Competition.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CompetitionDetailSerializer
        return CompetitionSerializer
