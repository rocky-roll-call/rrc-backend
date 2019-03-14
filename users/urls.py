# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path("", UserList.as_view()),
    path("create", UserCreate.as_view()),
    path("<int:pk>", UserRetrieveUpdate.as_view()),
    path("profiles", ProfileList.as_view()),
    path("profiles/<int:pk>", ProfileRetrieveUpdate.as_view()),
]
