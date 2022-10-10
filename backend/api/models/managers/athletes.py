"""Custom manager for Athlete model."""

from django.contrib.postgres.search import SearchHeadline, TrigramSimilarity
from django.db import models
from django.db.models import CharField, F
from django.db.models import Value as V
from django.db.models.functions import Concat


class AthleteManager(models.Manager):
    """Manager for the Athlete Model."""

    def search(self, query=None):
        """Search along name and location."""
        qs = self.get_queryset()
        if query is not None:
            qs = (
                qs.annotate(
                    name=Concat(
                        F("first_name"),
                        V(" "),
                        F("last_name"),
                        output_field=CharField(),
                    ),
                    similarity=TrigramSimilarity("name", query),
                    headline=SearchHeadline("name", query),
                )
                .filter(similarity__gte=0.3)
                .order_by("-similarity")
            )
        return qs
