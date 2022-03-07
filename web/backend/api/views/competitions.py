from rest_framework import viewsets

from api.models import Competition
from api.serializers import CompetitionSerializer, CompetitionDetailSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet for competitions
    """

    def get_queryset(self):
        return Competition.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            print("detail serializer")
            return CompetitionDetailSerializer
        return CompetitionSerializer
