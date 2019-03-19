from django.urls import path
from .views import (
    UserList,
    UserCreate,
    UserDestroy,
    UserRetrieveUpdate,
    ProfileList,
    ProfileRetrieveUpdate,
    UserPhotoListCreate,
    UserPhotoRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", UserList.as_view()),
    path("create", UserCreate.as_view()),
    path("<int:pk>", UserRetrieveUpdate.as_view()),
    path("<int:pk>/delete", UserDestroy.as_view()),
    path("profiles", ProfileList.as_view()),
    path("profiles/<int:pk>", ProfileRetrieveUpdate.as_view()),
    path("profiles/<int:pk>/photos", UserPhotoListCreate.as_view()),
    path("photos/<int:pk>", UserPhotoRetrieveUpdateDestroy.as_view()),
]
