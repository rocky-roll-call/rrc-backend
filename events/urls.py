from django.urls import path
from .views import (
    CastingListCreate,
    CastingRetrieveUpdateDestroy,
    EventListCreate,
    EventRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", EventListCreate.as_view(), name="events"),
    path("<int:pk>", EventRetrieveUpdateDestroy.as_view(), name="event"),
    path("<int:pk>/castings", CastingListCreate.as_view(), name="castings"),
    path(
        "<int:pk>/castings/<int:cid>",
        CastingRetrieveUpdateDestroy.as_view(),
        name="casting",
    ),
]
