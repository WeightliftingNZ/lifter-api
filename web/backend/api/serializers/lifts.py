from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField

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
        # fields = (
        #     "lift_id",
        #     "athlete",
        #     "competition",
        #     "snatch_first",
        #     "snatch_first_weight",
        #     "snatch_second",
        #     "snatch_second_weight",
        #     "snatch_third",
        #     "snatch_third_weight",
        # )
        fields = "__all__"
