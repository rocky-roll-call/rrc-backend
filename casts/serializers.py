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
            "created",
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
            "created",
            "managers",
            "members",
            "member_requests",
            "blocked",
            "future_events",
            "upcoming_events",
        )


class PageSectionSerializer(ModelSerializer):
    """
    A serializer for the casts.PageSection model
    """

    class Meta:
        model = PageSection
        fields = ("id", "cast", "title", "text", "order", "created")
        read_only_fields = ("cast", "created")


class CastPhotoSerializer(ModelSerializer):
    """
    A serializer for the casts.CastPhoto model
    """

    class Meta:
        model = CastPhoto
        fields = ("id", "cast", "image", "description", "created")
        read_only_fields = ("cast", "image", "created")
