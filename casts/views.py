"""
Cast API Views
"""

# django
from django.shortcuts import get_object_or_404

# library
from rest_framework import generics, permissions, views
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.response import Response

# app
from users.models import Profile
from .models import Cast, CastPhoto, PageSection
from .permissions import IsManager, IsManagerOrReadOnly
from .serializers import CastSerializer, CastPhotoSerializer, PageSectionSerializer


class CastListCreate(generics.ListCreateAPIView):
    """List available casts or create a new one"""

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
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
            raise ValidationError("User must be the sole manager to delete")
        instance.delete()


class ListManageView(views.APIView):
    """Add and remove objects from a list"""

    source: "Primary Model"
    member: "List Member Model"
    add_method: str
    remove_method: str

    permission_classes = (IsManager,)

    def _run(self, method: str, request, pk: int, pid: int) -> Response:
        source = get_object_or_404(self.source, pk=pk)
        self.check_object_permissions(request, source)
        member = get_object_or_404(self.member, pk=pid)
        try:
            getattr(source, method)(member)
            return Response()
        except ValueError as exc:
            raise ParseError(exc)

    def post(self, *args, **kwargs) -> Response:
        return self._run(self.add_method, *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self._run(self.remove_method, *args, **kwargs)


class CastMemberManager(ListManageView):

    source = Cast
    member = Profile
    add_method = "add_member"
    remove_method = "remove_member"


class CastManagerManager(ListManageView):

    source = Cast
    member = Profile
    add_method = "add_manager"
    remove_method = "remove_manager"


class CastMemberRequestManager(ListManageView):

    source = Cast
    member = Profile
    add_method = "add_member_request"
    remove_method = "remove_member_request"


class CastBlockedManager(ListManageView):

    source = Cast
    member = Profile
    add_method = "block_user"
    remove_method = "unblock_user"


class PageSectionListCreate(generics.ListCreateAPIView):
    """List all cast page sections or create a new one"""

    serializer_class = PageSectionSerializer
    permission_classes = (IsManagerOrReadOnly,)

    def get_queryset(self):
        return PageSection.objects.filter(cast=self.kwargs["pk"])

    def perform_create(self, serializer):
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

    def perform_create(self, serializer):
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
