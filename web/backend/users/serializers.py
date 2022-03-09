from rest_framework import serializers

from .models import CustomUser


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
