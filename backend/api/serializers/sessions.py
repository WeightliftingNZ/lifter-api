from cgitb import lookup

from hashid_field.rest import HashidSerializerCharField
from rest_framework import permissions, serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from api.models import Competition, Lift, Session

from .lifts import LiftSerializer


class SessionSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    lift_count = serializers.SerializerMethodField(read_only=True)

    def get_lift_count(self, session):
        return Lift.objects.filter(session=session).count()

    reference_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Session.reference_id",
        ),
        read_only=True,
    )

    competition = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="api.Competition.reference_id"),
        read_only=False,
        queryset=Competition.objects.all(),
    )

    competition_name = serializers.CharField(
        source="competition.competition_name", read_only=True
    )

    lift_set = LiftSerializer(many=True, read_only=True)

    # TODO: not giving url for sessions

    url = NestedHyperlinkedIdentityField(
        parent_lookup_kwargs={"competitions_pk": "competition__pk"},
        view_name="competition-sessions-detail",
    )

    class Meta:
        model = Session
        fields = (
            "url",
            "reference_id",
            "session_number",
            "session_datetime",
            "competition",
            "competition_name",
            "announcer",
            "referee_first",
            "referee_second",
            "referee_third",
            "technical_controller",
            "marshall",
            "timekeeper",
            "jury",
            "lift_count",
            "lift_set",
        )
