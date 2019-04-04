from django.urls import path
from .views import (
    CastListCreate,
    CastRetrieveUpdateDestroy,
    CastPhotoListCreate,
    CastPhotoRetrieveUpdateDestroy,
    PageSectionListCreate,
    PageSectionRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", CastListCreate.as_view(), name="casts"),
    path("<int:pk>", CastRetrieveUpdateDestroy.as_view(), name="cast"),
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
