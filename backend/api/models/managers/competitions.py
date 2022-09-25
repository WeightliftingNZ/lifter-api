"""Custom managers for Competitions model."""

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db import models
from django.db.models import Q


class CompetitionManager(models.Manager):
    """Manager for Competition Model."""

    def search(self, query=None):
        """Search along name and location."""
        qs = self.get_queryset()
        if query is not None:
            refined_query = SearchQuery(query)
            vector = SearchVector("name", "location")
            rank = SearchRank(vector, refined_query)
            name_headline = SearchHeadline(
                "name",
                refined_query,
            )
            location_headline = SearchHeadline("location", refined_query)

            qs = (
                qs.annotate(
                    search=vector,
                    rank=rank,
                    name_headline=name_headline,
                    location_headline=location_headline,
                )
                .filter(
                    Q(search=refined_query)
                    | Q(name__trigram_similar=query)
                    | Q(location__trigram_similar=query)
                )
                .distinct()
                .order_by("-rank")
            )
        return qs
