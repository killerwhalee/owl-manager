from rest_framework import serializers

from database.models import Problem
from user.serializer import UserSerializer


class ProblemSerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ["object", "id", "owner", "last_update"]

    def get_object(self, _):
        return "problem"
