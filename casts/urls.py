from django.urls import path
from .views import (
    CastListCreate,
    CastRetrieveUpdateDestroy,
    CastPhotoListCreate,
    CastPhotoRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", CastListCreate.as_view()),
    path("<int:pk>", CastRetrieveUpdateDestroy.as_view()),
    path("<int:pk>/photos", CastPhotoListCreate.as_view()),
    path("photos/<int:pk>", CastPhotoRetrieveUpdateDestroy.as_view()),
]
