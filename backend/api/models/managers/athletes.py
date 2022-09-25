"""Custom manager for Athlete model."""

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db import models
from django.db.models import Q


class AthleteManager(models.Manager):
    """Manager for the Athlete Model."""

    def search(self, query=None):
        """Search along name and location."""
        qs = self.get_queryset()
        if query is not None:
            refined_query = SearchQuery(query)
            vector = SearchVector("first_name", "last_name")
            rank = SearchRank(vector, refined_query)
            first_name_headline = SearchHeadline(
                "first_name",
                refined_query,
            )
            last_name_headline = SearchHeadline(
                "last_name",
                refined_query,
            )

            qs = (
                qs.annotate(
                    search=vector,
                    rank=rank,
                    first_name_headline=first_name_headline,
                    last_name_headline=last_name_headline,
                )
                .filter(
                    Q(search=refined_query)
                    | Q(first_name__trigram_similar=query)
                    | Q(last_name__trigram_similar=query)
                )
                .distinct()
                .order_by("-rank")
            )
        return qs
