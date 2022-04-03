from rest_framework import viewsets

from api.models import Lift
from api.serializers import LiftSerializer


class LiftViewSet(viewsets.ModelViewSet):
    """
    # Lift
    Each Session is composed of Lifts performed by Athletes.
    """

    def get_queryset(self):
        return Lift.objects.filter(
            session=self.kwargs["sessions_pk"],
        )

    def get_serializer_class(self):
        return LiftSerializer
