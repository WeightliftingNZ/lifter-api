from hashid_field.rest import HashidSerializerCharField
from rest_framework import permissions, serializers

from api.models import Athlete, Lift, Session


class LiftSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    reference_id = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Lift.reference_id",
        ),
        read_only=True,
    )

    athlete = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Athlete.reference_id",
        ),
        read_only=False,
        queryset=Athlete.objects.all(),
    )

    competition = HashidSerializerCharField(
        source="session.competition.reference_id", read_only=True
    )

    session = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Session.reference_id",
        ),
        read_only=False,
        queryset=Session.objects.all(),
    )

    athlete_name = serializers.CharField(
        source="athlete.full_name",
        read_only=True,
    )

    competition_name = serializers.CharField(
        source="session.competition.competition_name",
        read_only=True,
    )

    competition_date_start = serializers.CharField(
        source="session.competition.date_start",
        read_only=True,
    )

    class Meta:
        model = Lift
        fields = (
            "reference_id",
            "lottery_number",
            "athlete",
            "athlete_name",
            "competition",
            "session",
            "competition_name",
            "competition_date_start",
            "snatches",
            "best_snatch_weight",
            "cnjs",
            "best_cnj_weight",
            "total_lifted",
            "bodyweight",
            "weight_category",
            "team",
            "placing",
        )
