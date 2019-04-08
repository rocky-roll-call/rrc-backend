"""
Event API Views
"""

# library
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

# app
from casts.permissions import IsManagerOrReadOnly
from .models import Event, Casting
from .serializers import CastingSerializer, EventSerializer


class EventListCreate(generics.ListCreateAPIView):
    """List available events or create a new one"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)

    # def perform_create(self, serializer, format=None):
    #     pass


class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an event"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsManagerOrReadOnly,)


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
