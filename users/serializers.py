"""
Serializers to convert API data to and from the database
"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Profile, UserPhoto


class UserSerializer(ModelSerializer):
    """
    A serializer for the default auth.User model
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "last_login",
            "date_joined",
            "profile",
        )
        read_only_fields = ("id", "date_joined", "profile")
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
    A serializer for the users.Profile model
    """

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "name",
            "alt",
            "display_name",
            "age",
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
        read_only_fields = ("id", "user", "display_name", "age", "photos")


class PublicProfileSerializer(ModelSerializer):
    """
    A serializer for a user's public profile
    """

    class Meta:
        model = Profile
        fields = (
            "id",
            "display_name",
            "age",
            "image",
            "bio",
            "location",
            "external_url",
            "facebook_url",
            "twitter_user",
            "instagram_user",
            "photos",
        )


class UserPhotoSerializer(ModelSerializer):
    """
    A serializer for the users.UserPhoto model
    """

    class Meta:
        model = UserPhoto
        fields = ("id", "profile", "image", "description", "created")
        read_only_fields = ("id", "profile", "image", "created")
