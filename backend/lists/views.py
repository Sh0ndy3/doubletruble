from rest_framework import permissions, viewsets

from .models import List, Option
from .serializers import ListSerializer, OptionSerializer


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (List.objects.filter(
            couple__partner=self.request.user
        ) | List.objects.filter(
            couple__second_partner=self.request.user
        )).distinct()

    def perform_create(self, serializer):
        couple = serializer.validated_data["couple"]
        if not (
            couple.partner_id == self.request.user.user_id
            or couple.second_partner_id == self.request.user.user_id
        ):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only use your own couple.")
        serializer.save()


class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (Option.objects.filter(
            list__couple__partner=self.request.user
        ) | Option.objects.filter(
            list__couple__second_partner=self.request.user
        )).distinct()

    def perform_create(self, serializer):
        list_object = serializer.validated_data["list"]
        if not (
            list_object.couple.partner_id == self.request.user.user_id
            or list_object.couple.second_partner_id == self.request.user.user_id
        ):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only use your own couple.")
        serializer.save()
