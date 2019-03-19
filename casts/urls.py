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
    path("", CastListCreate.as_view()),
    path("<int:pk>", CastRetrieveUpdateDestroy.as_view()),
    path("<int:pk>/sections", PageSectionListCreate.as_view()),
    path("sections/<int:pk>", PageSectionRetrieveUpdateDestroy.as_view()),
    path("<int:pk>/photos", CastPhotoListCreate.as_view()),
    path("photos/<int:pk>", CastPhotoRetrieveUpdateDestroy.as_view()),
]
