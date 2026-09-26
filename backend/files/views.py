from rest_framework import permissions, viewsets

from .models import File
from .serializers import FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (File.objects.filter(
            couple__partner=self.request.user
        ) | File.objects.filter(
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
