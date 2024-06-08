from rest_framework import serializers

from user.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["object", "id", "user_email"]
        read_only_fields = ["object", "id", "user_email"]

    def get_object(self, _):
        return "user"


class ProfileSerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["object", "user", "date_joined", "user_image"]
        read_only_fields = ["object", "date_joined"]

    def get_object(self, _):
        return "profile"
