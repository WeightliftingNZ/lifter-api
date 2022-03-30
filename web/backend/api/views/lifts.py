from rest_framework import viewsets

from api.models import Lift
from api.serializers import LiftSerializer


class LiftViewSet(viewsets.ModelViewSet):
    """
    # ViewSet from lifters
    """

    # lookup_field = "lottery_number"

    def get_queryset(self):
        return Lift.objects.filter(
            # competition=self.kwargs["competitions_pk"],
            session=self.kwargs["sessions_pk"],
        )

    def get_serializer_class(self):
        return LiftSerializer
