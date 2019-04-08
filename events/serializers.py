"""
"""

from rest_framework.serializers import ModelSerializer
from .models import Event, Casting


class EventSerializer(ModelSerializer):
    """
    Serializer for the events.Event model
    """

    class Meta:
        model = Event
        fields = ("id", "cast", "name", "description", "venue", "start", "created")
        read_only_fields = ("id", "cast", "created")


class CastingSerializer(ModelSerializer):
    """
    Serializer for the events.Casting model
    """

    class Meta:
        model = Casting
        fields = ("id", "event", "profile", "role", "writein")
        read_only_fields = ("id", "event")
