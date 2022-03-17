from hashid_field.rest import HashidSerializerCharField
from rest_framework import permissions, serializers

from api.models import Athlete, Competition, Lift


class LiftSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    athlete = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Athlete.reference_id",
        ),
        read_only=False,
        queryset=Athlete.objects.all(),
    )
    competition = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="api.Competition.reference_id",
        ),
        read_only=False,
        queryset=Competition.objects.all(),
    )

    athlete_name = serializers.CharField(
        source="athlete.full_name",
        read_only=False,
    )
    competition_name = serializers.CharField(
        source="competition.competition_name",
        read_only=False,
    )

    competition_date_start = serializers.CharField(
        source="competition.date_start",
        read_only=False,
    )

    class Meta:
        model = Lift
        fields = (
            "reference_id",
            "athlete",
            "athlete_name",
            "competition",
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
            "lottery_number",
            "session_number",
            "session_datetime",
        )
