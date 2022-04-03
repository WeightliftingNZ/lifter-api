from collections import Counter

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.models import Competition, Session

from .sessions import SessionSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )
    reference_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Competition.reference_id",
        ),
        read_only=True,
    )

    session_count = serializers.SerializerMethodField(read_only=True)

    def get_session_count(self, competition):
        return Session.objects.filter(competition=competition).count()

    class Meta:
        model = Competition
        fields = (
            "url",
            "reference_id",
            "date_start",
            "date_end",
            "location",
            "competition_name",
            "session_count",
        )


class CompetitionDetailSerializer(CompetitionSerializer):
    session_set = SessionSerializer(many=True, read_only=True)

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + ("session_set",)
