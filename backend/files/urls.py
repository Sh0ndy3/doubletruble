from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import FileViewSet


router = DefaultRouter()
router.register("", FileViewSet, basename="file")

urlpatterns = [
    path("", include(router.urls)),
]
