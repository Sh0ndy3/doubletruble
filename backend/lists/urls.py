from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListViewSet, OptionViewSet


router = DefaultRouter()
router.register("options", OptionViewSet, basename="option")
router.register("", ListViewSet, basename="list")

urlpatterns = [
    path("", include(router.urls)),
]
