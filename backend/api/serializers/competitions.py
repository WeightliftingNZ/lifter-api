"""Competition Serializer."""

from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from api.models import Competition, Lift
from api.serializers.lifts import LiftSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )
    reference_id = serializers.PrimaryKeyRelatedField(  # type: ignore
        pk_field=HashidSerializerCharField(
            source_field="api.Competition.reference_id",
        ),
        read_only=True,
    )
    lifts_count = serializers.SerializerMethodField(read_only=True)

    def get_lifts_count(self, competition) -> int:
        return Lift.objects.filter(competition=competition).count()

    class Meta:
        model = Competition
        fields = [
            "url",
            "reference_id",
            "date_start",
            "date_end",
            "location",
            "name",
            "lifts_count",
        ]


class CompetitionDetailSerializer(CompetitionSerializer):
    # lift_set = LiftSerializer(many=True, read_only=True)
    lift_set = serializers.SerializerMethodField(read_only=True)

    def get_lift_set(self, competition):
        query = Lift.objects.ordered_filter(competition=competition)
        return LiftSerializer(
            query, many=True, read_only=True, context=self.context
        ).data

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + [
            "lift_set",
        ]
