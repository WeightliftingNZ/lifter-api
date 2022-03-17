from rest_framework import filters, viewsets

from api.models import Competition
from api.serializers import CompetitionDetailSerializer, CompetitionSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet for competitions
    """

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["competition_name", "location"]
    ordering_fields = ["date_start"]
    ordering = ["-date_start"]

    def get_queryset(self):
        return Competition.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CompetitionDetailSerializer
        return CompetitionSerializer
