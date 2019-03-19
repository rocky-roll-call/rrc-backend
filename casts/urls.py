from django.urls import path
from .views import CastListCreate, CastRetrieveUpdateDestroy

urlpatterns = [
    path("", CastListCreate.as_view()),
    path("<int:pk>", CastRetrieveUpdateDestroy.as_view()),
]
