from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("home/", views.home, name="home"),
]