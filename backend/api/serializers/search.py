"""Search serializers."""

import re

from rest_framework import serializers

from api.models import Athlete, Competition, Lift
from api.serializers import (
    AthleteSerializer,
    CompetitionSerializer,
    LiftSerializer,
)


class SearchSerializer(serializers.Serializer):

    query_result_type = serializers.SerializerMethodField(read_only=True)
    query_result = serializers.SerializerMethodField(read_only=True)
    query_result_headline = serializers.SerializerMethodField(read_only=True)
    query_result_headline_no_html = serializers.SerializerMethodField(
        read_only=True
    )

    def get_query_result_type(self, instance):
        """Give the type of result (e.g. "Athlete", "Lift", "Competition")."""
        response = instance.__class__.__name__
        return response

    def _get_headline_attributes(self, instance):
        headlines = [
            getattr(instance, headline)
            for headline in dir(instance)
            if "headline" in headline
        ]
        return headlines

    def get_query_result_headline_no_html(self, instance):
        """Return a the search headline without html."""
        TAG_RE = re.compile(r"<[^>]+>")
        return TAG_RE.sub("", instance.headline)

    def get_query_result_headline(self, instance):
        """Return the search headline with <b></b> highligiting."""
        return instance.headline

    def get_query_result(self, instance):
        """Utilises serializers for combined search queryset."""
        if isinstance(instance, Athlete):
            return AthleteSerializer(
                instance, read_only=True, context=self.context
            ).data
        elif isinstance(instance, Competition):
            return CompetitionSerializer(
                instance, read_only=True, context=self.context
            ).data
        elif isinstance(instance, Lift):
            return LiftSerializer(
                instance, read_only=True, context=self.context
            ).data
