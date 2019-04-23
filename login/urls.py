from django.urls import path
from .views import facebook_login

urlpatterns = [path("login/facebook", facebook_login, name="facebook-login")]
