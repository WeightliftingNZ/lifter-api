from config.settings.base import HASHID_FIELD_SALT
from django.db import models
from django.utils.functional import cached_property
from hashid_field import HashidAutoField


class Session(models.Model):
    # assigned a number
    reference_id = HashidAutoField(
        primary_key=True, salt=f"sessionmodel_reference_id_{HASHID_FIELD_SALT}"
    )
    session_datetime = models.DateTimeField(blank=True)
    competition = models.ForeignKey("api.Competition", on_delete=models.CASCADE)

    # officials
    referee_first = models.CharField(max_length=128, blank=True)
    referee_second = models.CharField(max_length=128, blank=True)
    referee_third = models.CharField(max_length=128, blank=True)
    technical_controller = models.CharField(max_length=128, blank=True)
    marshall = models.CharField(max_length=255, blank=True)
    timekeeper = models.CharField(max_length=255, blank=True)
    announcer = models.CharField(max_length=255, blank=True)
    jury = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["session_datetime"]

    @cached_property
    def session_number(self) -> int:
        """This is the session number, which is the order determined by the date/time of the session

        Returns:
            int: return the session number in the competition
        """
        query = Session.objects.filter(competition=self.competition)
        sessions = [(q.reference_id, q.session_datetime) for q in query]
        sessions.sort(key=lambda x: x[1])
        sessions_reference_ids = [session[0] for session in sessions]
        return sessions_reference_ids.index(self.reference_id) + 1

    def __str__(self):
        return f"{self.competition} {self.competition.date_start.year} - {self.session_number}"
