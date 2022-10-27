"""Custom managers for Competitions model."""

from datetime import datetime

from django.contrib.postgres.search import SearchHeadline, TrigramSimilarity
from django.db import models
from django.db.models import CharField, F
from django.db.models import Value as V
from django.db.models.functions import Concat


class CompetitionManager(models.Manager):
    """Manager for Competition Model."""

    def search(self, query=None):
        """Search along name and location."""
        qs = self.get_queryset()
        if query is not None:
            qs = (
                qs.annotate(
                    name_location=Concat(
                        F("name"),
                        V(" "),
                        F("location"),
                        output_filed=CharField(),
                    ),
                    similarity=TrigramSimilarity("name_location", query),
                    headline=SearchHeadline("name_location", query),
                )
                .filter(similarity__gte=0.3)
                .order_by("-similarity")
            )
        return qs

    def year(self, query=None):
        """Search competition year."""
        qs = self.get_queryset()
        if query is not None:
            qs = qs.filter(
                date_start__gte=datetime(query, 1, 1),
                date_start__lte=datetime(query, 12, 31),
            )
        return qs
