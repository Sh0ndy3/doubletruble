from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import CalendarPlan, Color, Plan, Repeat
from .serializers import (
    CalendarPlanSerializer,
    ColorSerializer,
    PlanSerializer,
    RepeatSerializer,
)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]


class RepeatViewSet(viewsets.ModelViewSet):
    queryset = Repeat.objects.all()
    serializer_class = RepeatSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (Plan.objects.filter(
            couple__partner=self.request.user
        ) | Plan.objects.filter(
            couple__second_partner=self.request.user
        )).distinct()

    def perform_create(self, serializer):
        couple = serializer.validated_data["couple"]
        if not (
            couple.partner_id == self.request.user.user_id
            or couple.second_partner_id == self.request.user.user_id
        ):
            raise PermissionDenied("You can only use your own couple.")
        serializer.save()


class CalendarPlanViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (CalendarPlan.objects.filter(
            plan__couple__partner=self.request.user
        ) | CalendarPlan.objects.filter(
            plan__couple__second_partner=self.request.user
        )).distinct()

    def perform_create(self, serializer):
        plan = serializer.validated_data["plan"]
        if not (
            plan.couple.partner_id == self.request.user.user_id
            or plan.couple.second_partner_id == self.request.user.user_id
        ):
            raise PermissionDenied("You can only use your own couple.")
        serializer.save()
