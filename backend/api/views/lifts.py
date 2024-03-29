"""Lift viewset."""

from rest_framework import viewsets

from api.models import Lift
from api.serializers import LiftSerializer


class LiftViewSet(viewsets.ModelViewSet):
    """
    # Lift

    """

    def get_queryset(self):
        return Lift.objects.filter(
            competition=self.kwargs["competitions_pk"],
        )

    def get_serializer_class(self):
        return LiftSerializer
