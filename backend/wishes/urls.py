from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    WishPhotoDetailAPIView,
    WishPhotoListCreateAPIView,
    WishViewSet,
)


router = DefaultRouter()
router.register("", WishViewSet, basename="wish")

urlpatterns = [
    path("<uuid:wish_id>/photos/", WishPhotoListCreateAPIView.as_view()),
    path(
        "<uuid:wish_id>/photos/<int:photo_id>/",
        WishPhotoDetailAPIView.as_view(),
    ),
    path("", include(router.urls)),
]
