from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CoupleInviteAPIView,
    CoupleJoinAPIView,
    CoupleStatsAPIView,
    CoupleViewSet,
)


router = DefaultRouter()
router.register("", CoupleViewSet, basename="couple")

urlpatterns = [
    path("invite/", CoupleInviteAPIView.as_view(), name="couple-invite"),
    path("join/", CoupleJoinAPIView.as_view(), name="couple-join"),
    path("stats/", CoupleStatsAPIView.as_view(), name="couple-stats"),
    path("", include(router.urls)),
]
