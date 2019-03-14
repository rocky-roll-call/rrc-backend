"""
User API Views
"""

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Profile
from .serializers import *


class UserList(generics.ListAPIView):
    """View to list all users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserCreate(generics.CreateAPIView):
    """View to create a new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Retrieve a user or update user information"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileList(generics.ListAPIView):
    """View to list all user profiles"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """Retrieve a user profile or update its information"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
