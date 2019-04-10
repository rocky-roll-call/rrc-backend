"""
Event API Views
"""

# django
from django.shortcuts import get_object_or_404

# library
from rest_framework import generics
from rest_framework.exceptions import ValidationError

# app
from casts.models import Cast
from casts.permissions import IsManagerOrReadOnly
from users.models import Profile
from .models import Event, Casting
from .serializers import CastingSerializer, EventSerializer


class EventListCreate(generics.ListCreateAPIView):
    """List available events or create a new one"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_create(self, serializer):
        cast = get_object_or_404(Cast, pk=self.request.data["cast"])
        self.check_object_permissions(self.request, cast)
        serializer.save(cast=cast)


class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_update(self, serializer):
        if "cast" in self.request.data:
            raise ValidationError(
                "You cannot change the cast after an event has been created"
            )
        serializer.save()


class CastingListCreate(generics.ListCreateAPIView):
    """List available events or create a new one"""

    serializer_class = CastingSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def get_queryset(self):
        return Casting.objects.filter(event=self.kwargs["pk"])

    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, event)
        if "profile" in self.request.data:
            profile = get_object_or_404(Profile, pk=self.request.data["profile"])
            if not event.cast.is_member(profile):
                raise ValidationError(f"{profile} is not a member of {event.cast}")
            serializer.save(event=event, profile=profile)
        serializer.save(event=event)


class CastingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event casting"""

    queryset = Casting.objects.all()
    serializer_class = CastingSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_update(self, serializer):
        if "event" in self.request.data:
            raise ValidationError(
                "You cannot change the event after a casting has been created"
            )
        if "profile" in self.request.data:
            profile = get_object_or_404(Profile, pk=self.request.data["profile"])
            cast = self.get_object().event.cast
            if not cast.is_member(profile):
                raise ValidationError(f"{profile} is not a member of {cast}")
            serializer.save(profile=profile)
        serializer.save()
