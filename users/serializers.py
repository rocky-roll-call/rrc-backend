"""
Serializers to convert API data to and from the database
"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Profile, UserPhoto


class UserSerializer(ModelSerializer):
    """
    A serializer for the default User model
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "profile")
        read_only_fields = ("id", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            password=make_password(validated_data["password"]),
        )
        user.save()
        return user


class ProfileSerializer(ModelSerializer):
    """
    A serializer for the Profile model
    """

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "name",
            "age",
            "full_name",
            "alt",
            "image",
            "bio",
            "location",
            "external_url",
            "facebook_url",
            "twitter_user",
            "instagram_user",
            "show_email",
            "searchable",
            "email_confirmed",
            "birth_date",
            "photos",
        )
        read_only_fields = ("id", "user", "name", "age", "photos")


class UserPhotoSerializer(ModelSerializer):
    """
    A serializer for the UserPhoto model
    """

    class Meta:
        model = UserPhoto
        fields = ("id", "profile", "image", "description", "created_date")
        read_only_fields = ("id", "profile", "image", "created_date")
