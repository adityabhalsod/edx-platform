"""
Serializers for the User Profiles API.
"""

from rest_framework import serializers

from cms.djangoapps.user_profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "avatar_url",
            "date_of_birth",
            "phone_number",
            "city",
            "country",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
