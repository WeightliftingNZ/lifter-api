from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.models import AthleteModel, CompetitionModel, SessionModel, LifterModel


class AthleteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="athletes-detail", read_only=True
    )

    class Meta:
        model = AthleteModel
        fields = ("url", "first_name", "last_name", "yearborn")


class SessionSerializer(serializers.ModelSerializer):
    competition = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.CompetitionModel.reference_id"
        ),
        read_only=True,
    )
    url = serializers.HyperlinkedRelatedField(
        view_name="competition-sessions-detail",
        read_only=True,
    )

    class Meta:
        model = SessionModel
        fields = ("url", "date", "competition")


class CompetitionSessionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {"competition_pk": "competition__pk"}

    class Meta:
        model = SessionModel
        fields = ("url", "date")


class CompetitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="competitions-detail", read_only=True
    )

    class Meta:
        model = CompetitionModel
        fields = (
            "url",
            "date_start",
            "date_end",
            "location",
            "competition_name",
        )


class CompetitionDetailSerializer(CompetitionSerializer):
    sessions = CompetitionSessionSerializer(many=True, read_only=True)

    class Meta(CompetitionSerializer.Meta):
        fields = CompetitionSerializer.Meta.fields + ("sessions",)


class LifterSerializer(serializers.ModelSerializer):
    model = LifterModel
