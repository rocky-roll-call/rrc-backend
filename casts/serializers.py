"""
"""

from rest_framework.serializers import ModelSerializer
from .models import Cast, CastPhoto, PageSection


class CastSerializer(ModelSerializer):
    """
    Serializer for the casts.Cast model
    """

    class Meta:
        model = Cast
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "email",
            "created_date",
            "external_url",
            "facebook_url",
            "twitter_user",
            "instagram_user",
            "managers",
            "members",
            "member_requests",
            "blocked",
            "future_events",
            "upcoming_events",
        )
        read_only_fields = (
            "slug",
            "created_date",
            "managers",
            "members",
            "member_requests",
            "blocked",
            "future_events",
            "upcoming_events",
        )


class CastPhotoSerializer(ModelSerializer):
    """
    A serializer for the casts.CastPhoto model
    """

    class Meta:
        model = CastPhoto
        fields = ("id", "cast", "image", "description", "created_date")
        read_only_fields = ("id", "cast", "image", "created_date")
