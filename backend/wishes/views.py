from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wish, WishPhoto
from .serializers import WishesPhotoSerializer, WishesSerializer


class WishViewSet(viewsets.ModelViewSet):
    serializer_class = WishesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (Wish.objects.filter(
            couple__partner=self.request.user
        ) | Wish.objects.filter(
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


class WishPhotoListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_wish(self, wish_id, user):
        try:
            return Wish.objects.get(
                wish_id=wish_id
            )
        except Wish.DoesNotExist:
            return None

    def has_access(self, wish, user):
        return (
            wish.couple.partner_id == user.user_id
            or wish.couple.second_partner_id == user.user_id
        )

    def get(self, request, wish_id):
        wish = self.get_wish(wish_id, request.user)
        if wish is None or not self.has_access(wish, request.user):
            return Response(
                {"detail": "Wish not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            WishesPhotoSerializer(wish.photos.all(), many=True).data
        )

    def post(self, request, wish_id):
        wish = self.get_wish(wish_id, request.user)
        if wish is None or not self.has_access(wish, request.user):
            return Response(
                {"detail": "Wish not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = WishesPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = WishPhoto.objects.create(
            wish=wish,
            wish_photo_link=serializer.validated_data["wish_photo_link"],
        )

        return Response(
            WishesPhotoSerializer(photo).data,
            status=status.HTTP_201_CREATED,
        )


class WishPhotoDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_photo(self, wish_id, photo_id):
        try:
            return WishPhoto.objects.select_related(
                "wish__couple"
            ).get(
                id=photo_id,
                wish_id=wish_id,
            )
        except WishPhoto.DoesNotExist:
            return None

    def has_access(self, photo, user):
        return (
            photo.wish.couple.partner_id == user.user_id
            or photo.wish.couple.second_partner_id == user.user_id
        )

    def delete(self, request, wish_id, photo_id):
        photo = self.get_photo(wish_id, photo_id)
        if photo is None or not self.has_access(photo, request.user):
            return Response(
                {"detail": "Photo not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
