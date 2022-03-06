from rest_framework import viewsets

from api.models import CompetitionModel, SessionModel, LifterModel, AthleteModel

from api.serializers import (
    CompetitionSerializer,
    CompetitionDetailSerializer,
    SessionSerializer,
    LifterSerializer,
    AthleteSerializer,
)


class AthleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for athlete
    ===================
    """

    def get_queryset(self):
        return AthleteModel.objects.all()

    def get_serializer_class(self):
        return AthleteSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet for competitions
    """

    def get_queryset(self):
        return CompetitionModel.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CompetitionDetailSerializer
        return CompetitionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet from session
    """

    def get_queryset(self):
        return SessionModel.objects.filter(competition=self.kwargs["competition_pk"])

    def get_serializer_class(self):
        return SessionSerializer


class LifterViewSet(viewsets.ModelViewSet):
    """
    # ViewSet from lifters
    """

    def get_queryset(self):
        return LifterModel.objects.filter(athlete=self.kwargs["athlete_pk"])

    def get_serializer_class(self):
        return LifterSerializer
