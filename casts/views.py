"""
Cast API Views
"""

from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError
from .models import Cast, CastPhoto, PageSection
from .serializers import CastSerializer, CastPhotoSerializer


class CastListCreate(generics.ListCreateAPIView):
    """List available casts or create a new one"""

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CastRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cast"""

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CastPhotoListCreate(generics.ListCreateAPIView):
    """List all cast photos or create a new one"""

    serializer_class = CastPhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CastPhoto.objects.filter(cast=self.kwargs["pk"])

    def perform_create(self, serializer, format=None):
        cast = Cast.objects.get(pk=self.kwargs["pk"])
        image = self.request.data.get("image")
        if image is None:
            raise ParseError("Could not find an 'image' in the POST data")
        serializer.save(image=image, cast=cast)


class CastPhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cast photo"""

    queryset = CastPhoto.objects.all()
    serializer_class = CastPhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)
