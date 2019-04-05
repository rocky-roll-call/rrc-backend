from django.urls import path
from .views import (
    CastListCreate,
    CastRetrieveUpdateDestroy,
    CastMemberManager,
    CastManagerManager,
    CastMemberRequestManager,
    CastBlockedManager,
    CastPhotoListCreate,
    CastPhotoRetrieveUpdateDestroy,
    PageSectionListCreate,
    PageSectionRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", CastListCreate.as_view(), name="casts"),
    path("<int:pk>", CastRetrieveUpdateDestroy.as_view(), name="cast"),
    path("<int:pk>/members/<int:pid>", CastMemberManager.as_view(), name="cast-member"),
    path(
        "<int:pk>/managers/<int:pid>", CastManagerManager.as_view(), name="cast-manager"
    ),
    path(
        "<int:pk>/member-requests/<int:pid>",
        CastMemberRequestManager.as_view(),
        name="cast-member-request",
    ),
    path(
        "<int:pk>/blocked/<int:pid>", CastBlockedManager.as_view(), name="cast-blocked"
    ),
    path(
        "<int:pk>/sections", PageSectionListCreate.as_view(), name="cast-page-sections"
    ),
    path(
        "sections/<int:pk>",
        PageSectionRetrieveUpdateDestroy.as_view(),
        name="cast-page-section",
    ),
    path("<int:pk>/photos", CastPhotoListCreate.as_view(), name="cast-photos"),
    path(
        "photos/<int:pk>", CastPhotoRetrieveUpdateDestroy.as_view(), name="cast-photo"
    ),
]
