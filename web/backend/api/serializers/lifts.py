from rest_framework import serializers

from api.models import Lift


class LiftSerializer(serializers.ModelSerializer):

    athlete = serializers.HyperlinkedRelatedField(
        view_name="athletes-detail",
        read_only=True,
    )

    competition = serializers.HyperlinkedRelatedField(
        view_name="competitions-detail",
        read_only=True,
    )

    class Meta:
        model = Lift
        fields = "__all__"
