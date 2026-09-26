from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CalendarPlanViewSet,
    ColorViewSet,
    PlanViewSet,
    RepeatViewSet,
)


router = DefaultRouter()
router.register("colors", ColorViewSet, basename="color")
router.register("repeats", RepeatViewSet, basename="repeat")
router.register("calendar-plans", CalendarPlanViewSet, basename="calendar-plan")
router.register("", PlanViewSet, basename="plan")

urlpatterns = [
    path("", include(router.urls)),
]
