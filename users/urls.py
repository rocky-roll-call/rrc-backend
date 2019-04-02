from django.urls import path
from .views import (
    UserList,
    UserCreate,
    UserRetrieveUpdateDestroy,
    ProfileList,
    ProfileRetrieveUpdate,
    UserPhotoListCreate,
    UserPhotoRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", UserList.as_view(), name="users"),
    path("create", UserCreate.as_view()),
    path("<int:pk>", UserRetrieveUpdateDestroy.as_view(), name="user"),
    path("profiles", ProfileList.as_view(), name="profiles"),
    path("profiles/<int:pk>", ProfileRetrieveUpdate.as_view(), name="profile"),
    path(
        "profiles/<int:pk>/photos", UserPhotoListCreate.as_view(), name="profile-photos"
    ),
    path(
        "photos/<int:pk>",
        UserPhotoRetrieveUpdateDestroy.as_view(),
        name="profile-photo",
    ),
]
