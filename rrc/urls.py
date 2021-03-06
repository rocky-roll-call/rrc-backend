"""rrc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, static

import rest_framework_jwt.views as jwt_views

# app
from casts.views import CastListCreate
from events.views import EventListCreate

urlpatterns = [
    path("admin", admin.site.urls),
    path("auth/", include("rest_auth.urls")),
    path("auth/registration/", include("rest_auth.registration.urls")),
    # path("auth/social/", include("login.urls")),
    path("auth/token", jwt_views.obtain_jwt_token),
    path("auth/token/refresh", jwt_views.refresh_jwt_token),
    path("users/", include("users.urls")),
    path("casts", CastListCreate.as_view(), name="casts"),
    path("casts/", include("casts.urls")),
    path("events", EventListCreate.as_view(), name="events"),
    path("events/", include("events.urls")),
]

if settings.MEDIA_URL:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
