"""
User API Views
"""

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.exceptions import ParseError, PermissionDenied
from .permissions import IsOwnerOrReadOnly, IsUser
from .models import Profile, UserPhoto
from .serializers import (
    ProfileSerializer,
    PublicProfileSerializer,
    UserSerializer,
    UserPhotoSerializer,
)


class UserList(generics.ListAPIView):
    """View to list all users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


# THIS WILL BE REPLACED. NO TESTS NEEDED
class UserCreate(generics.CreateAPIView):
    """View to create a new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve a user or update user information"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)

    def perform_update(self, serializer, format=None):
        image = self.request.data.get("image")
        if image is not None:
            serializer.save(image=image)
        else:
            serializer.save()


class ProfileList(generics.ListAPIView):
    """View to list all user profiles"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Retrieve a user profile or update its information"""

    queryset = Profile.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.kwargs["pk"] == self.request.user.profile.pk:
            return ProfileSerializer
        return PublicProfileSerializer


class UserPhotoListCreate(generics.ListCreateAPIView):
    """List all user photos or create a new one"""

    serializer_class = UserPhotoSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return UserPhoto.objects.filter(profile=self.kwargs["pk"])

    def perform_create(self, serializer, format=None):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, profile)
        if profile.user != self.request.user:
            raise PermissionDenied()
        image = self.request.data.get("image")
        if image is None:
            raise ParseError("Could not find an 'image' in the POST data")
        serializer.save(image=image, profile=profile)


class UserPhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a user photo"""

    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer
    permission_classes = (IsOwnerOrReadOnly,)
