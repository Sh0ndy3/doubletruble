from django.urls import path

from .views import ChangePasswordAPIView, LoginAPIView, LogoutAPIView


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
]
