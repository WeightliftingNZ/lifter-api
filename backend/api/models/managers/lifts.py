"""Custom managers for Lift model."""

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db import models
from django.db.models import Q


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
            refined_query = SearchQuery(query)
            vector = SearchVector(
                "athlete__first_name",
                "athlete__last_name",
            )
            rank = SearchRank(vector, refined_query)
            first_name_headline = SearchHeadline(
                "athlete__first_name",
                refined_query,
            )
            last_name_headline = SearchHeadline(
                "athlete__last_name", refined_query
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
                    | Q(athlete__first_name__trigram_similar=query)
                    | Q(athlete__last_name__trigram_similar=query)
                )
                .distinct()
                .order_by("-rank")
            )
        return qs
