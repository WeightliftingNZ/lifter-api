from rest_framework import viewsets, permissions

from api.models import Athlete
from api.serializers import AthleteSerializer, AthleteDetailSerializer


class AthleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for athlete
    ===================
    This contains all the athlete's details
    Can be used to access all lifts from previous competitions
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Athlete.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AthleteDetailSerializer
        return AthleteSerializer
