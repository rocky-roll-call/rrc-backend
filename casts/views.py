"""
Cast API Views
"""

from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError
from .models import Cast, CastPhoto, PageSection
from .permissions import IsManagerOrReadOnly
from .serializers import CastSerializer, CastPhotoSerializer, PageSectionSerializer


class CastListCreate(generics.ListCreateAPIView):
    """List available casts or create a new one"""

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer, format=None):
        cast = serializer.save()
        cast.add_member(self.request.user.profile)
        cast.add_manager(self.request.user.profile)


class CastRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cast"""

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def perform_destroy(self, instance: Cast):
        if instance.managers.count() > 1:
            raise ParseError("User must be the sole manager to delete")
        instance.delete()


class PageSectionListCreate(generics.ListCreateAPIView):
    """List all cast page sections or create a new one"""

    serializer_class = PageSectionSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def get_queryset(self):
        return PageSection.objects.filter(cast=self.kwargs["pk"])

    def perform_create(self, serializer, format=None):
        cast = Cast.objects.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, cast)
        serializer.save(cast=cast)


class PageSectionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cast photo"""

    queryset = PageSection.objects.all()
    serializer_class = PageSectionSerializer
    permission_classes = (IsManagerOrReadOnly,)


class CastPhotoListCreate(generics.ListCreateAPIView):
    """List all cast photos or create a new one"""

    serializer_class = CastPhotoSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def get_queryset(self):
        return CastPhoto.objects.filter(cast=self.kwargs["pk"])

    def perform_create(self, serializer, format=None):
        cast = Cast.objects.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, cast)
        image = self.request.data.get("image")
        if image is None:
            raise ParseError("Could not find an 'image' in the POST data")
        serializer.save(image=image, cast=cast)


class CastPhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cast photo"""

    queryset = CastPhoto.objects.all()
    serializer_class = CastPhotoSerializer
    permission_classes = (IsManagerOrReadOnly,)
