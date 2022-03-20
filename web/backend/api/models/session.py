from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Session(models.Model):
    # TODO: Need to write a session table
    # assigned a number
    reference_id = models.AutoField(primary_key=True)
    session_datetime = models.DateTimeField(blank=True)
    competition = models.ForeignKey(
        "api.Competition", on_delete=models.CASCADE
    )

    # officials
    referee_first = models.CharField(max_length=128, blank=True)
    referee_second = models.CharField(max_length=128, blank=True)
    referee_third = models.CharField(max_length=128, blank=True)
    technical_controller = models.CharField(max_length=128, blank=True)
    marshall = models.CharField(max_length=255, blank=True)
    timekeeper = models.CharField(max_length=255, blank=True)
    announcer = models.CharField(max_length=255, blank=True)
    jury = models.CharField(max_length=255, blank=True)

    @cached_property
    def session_number(self) -> int:
        """This is used for the url

        Returns:
            int: return the session number in the competition
        """
        query = Session.objects.filter(competition=self.competition)
        sessions = [q.reference_id for q in query]
        sessions.sort()
        return sessions.index(self.reference_id) + 1

    def __str__(self):
        return f"{self.competition} {self.competition.date_start.year} - {self.session_number}"
