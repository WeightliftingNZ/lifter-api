"""Custom managers for Lift model."""

from django.contrib.postgres.search import SearchHeadline, TrigramSimilarity
from django.db import models
from django.db.models import CharField, F
from django.db.models import Value as V
from django.db.models.functions import Concat


class LiftManager(models.Manager):
    """Lift Manager for Lift Model."""

    def ordered_filter(self, *args, **kwargs):
        """Order lift by weight category specifics.

        1. Weightclasses
        2. Super-heavies
        3. Female before male
        """
        kwargs.get("competition")
        query = super().filter(*args, **kwargs)

        # order on int values for weight classes (i.e. not string)
        query = sorted(  # type: ignore
            query, key=lambda q: int(q.weight_category[1:].replace("+", ""))
        )
        # ordering super heavies
        query = sorted(query, key=lambda q: "+" in q.weight_category)  # type: ignore
        # order female before male
        query = sorted(query, key=lambda q: q.weight_category[0], reverse=True)  # type: ignore

        return query

    def search(self, query=None):
        """Search along name and location."""
        qs = self.get_queryset()
        if query is not None:
            qs = (
                qs.annotate(
                    athlete_name=Concat(
                        F("athlete__first_name"),
                        V(" "),
                        F("athlete__last_name"),
                        output_field=CharField(),
                    ),
                    similarity=TrigramSimilarity("athlete_name", query),
                    headline=SearchHeadline("athlete_name", query),
                )
                .filter(similarity__gte=0.3)
                .order_by("-similarity")
            )
        return qs
