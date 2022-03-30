from rest_framework import viewsets

from api.models import Session
from api.serializers import SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """
    # ViewSet for sessions
    - A session is part of a competition. Session will contain all the lifts for that particular competition as well the officials responsible for that session
    - Anyone:
        - list
        - retrieve
    - User only:
        - create
        - update
        - delete
    """

    # lookup_field = "session_number"
    # I want to make session_number the url look up
    # but I don't know how to do this

    def get_queryset(self):
        return Session.objects.filter(
            competition=self.kwargs["competitions_pk"],
        )

    def get_serializer_class(self):
        return SessionSerializer
