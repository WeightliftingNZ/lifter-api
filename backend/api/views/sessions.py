from rest_framework import viewsets

from api.models import Session
from api.serializers import SessionSerializer


class SessionViewSet(viewsets.ModelViewSet):
    """
    # Session
    - A Session is part of a competition. Session will contain all the lifts for that particular competition as well the officials responsible for that session.

    - Officials:
        - 1st Referee, 2nd Referee (or center), 3rd Referee
        - Timekeeper, Announcer
        - Jury

    - Conditions:
        1. A single Session can only be in one competition.
    """

    def get_queryset(self):
        return Session.objects.filter(
            competition=self.kwargs["competitions_pk"],
        )

    def get_serializer_class(self):
        return SessionSerializer
