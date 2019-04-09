"""
Event API Views
"""

# django
from django.shortcuts import get_object_or_404

# library
from rest_framework import generics

# app
from casts.models import Cast
from casts.permissions import IsManagerOrReadOnly
from .models import Event, Casting
from .serializers import CastingSerializer, EventSerializer


class EventListCreate(generics.ListCreateAPIView):
    """List available events or create a new one"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_create(self, serializer, format=None):
        cast = get_object_or_404(Cast, pk=self.request.data["cast"])
        self.check_object_permissions(self.request, cast)
        serializer.save(cast=cast)


class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_update(self, serializer, format=None):
        if "cast" in self.request.data:
            cast = get_object_or_404(Cast, pk=self.request.data["cast"])
            self.check_object_permissions(self.request, cast)
            serializer.save(cast=cast)
        else:
            serializer.save()


class CastingListCreate(generics.ListCreateAPIView):
    """List available events or create a new one"""

    serializer_class = CastingSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def get_queryset(self):
        return Casting.objects.filter(event=self.kwargs["pk"])

    # def perform_create(self, serializer, format=None):
    #     pass


class CastingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event casting"""

    queryset = Casting.objects.all()
    serializer_class = CastingSerializer
    permission_classes = (IsManagerOrReadOnly,)
