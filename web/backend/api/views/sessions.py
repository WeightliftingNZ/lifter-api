from rest_framework import viewsets

from api.models import Session
from api.serializers import SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet for sessions
    - A session is part of a competition.
    - Anyone:
        - list
        - retrieve
    - User only:
        - create
        - update
        - delete
    """

    def get_queryset(self):
        print(self.kwargs)
        return Session.objects.filter(
            competition=self.kwargs["competitions_pk"]
        )

    def get_serializer_class(self):
        return SessionSerializer
