from datetime import date

from django.core.cache import cache
from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import secrets

from users.models import User

from .models import Couple
from .serializers import CoupleCreateSerializer, CoupleSerializer


def user_couple_queryset(user):
    return Couple.objects.filter(
        partner=user
    ) | Couple.objects.filter(
        second_partner=user
    )


class CoupleViewSet(viewsets.ModelViewSet):
    serializer_class = CoupleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return user_couple_queryset(self.request.user).distinct()

    def create(self, request, *args, **kwargs):
        serializer = CoupleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        second_partner = User.objects.get(
            user_id=serializer.validated_data["second_partner"]
        )
        if second_partner.user_id == request.user.user_id:
            return Response(
                {"detail": "You cannot create a couple with yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_couple_queryset(request.user).exists():
            return Response(
                {"detail": "You already belong to a couple."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_couple_queryset(second_partner).exists():
            return Response(
                {"detail": "This user already belongs to a couple."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        couple = Couple.objects.create(
            partner=request.user,
            second_partner=second_partner,
            date_of_start=serializer.validated_data["date_of_start"],
        )
        return Response(
            CoupleSerializer(couple).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        couple = self.get_object()
        couple.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoupleInviteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if user_couple_queryset(request.user).exists():
            return Response(
                {"detail": "You already belong to a couple."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = f"{secrets.randbelow(900000) + 100000}"
        cache.set(
            f"couple_invite:{code}",
            str(request.user.user_id),
            timeout=600,
        )
        return Response({"code": code, "expires_in": 600})


class CoupleJoinAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        code = str(request.data.get("code", ""))
        date_of_start = request.data.get("date_of_start")

        if not code or not date_of_start:
            return Response(
                {"detail": "code and date_of_start are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_couple_queryset(request.user).exists():
            return Response(
                {"detail": "You already belong to a couple."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inviter_id = cache.get(f"couple_invite:{code}")
        if inviter_id is None:
            return Response(
                {"detail": "Invalid or expired invite code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(request.user.user_id) == str(inviter_id):
            return Response(
                {"detail": "You cannot join your own invite."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inviter = User.objects.get(user_id=inviter_id)
        if user_couple_queryset(inviter).exists():
            cache.delete(f"couple_invite:{code}")
            return Response(
                {"detail": "The invite owner already belongs to a couple."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        couple = Couple.objects.create(
            partner=inviter,
            second_partner=request.user,
            date_of_start=date_of_start,
        )
        cache.delete(f"couple_invite:{code}")

        return Response(
            CoupleSerializer(couple).data,
            status=status.HTTP_201_CREATED,
        )


class CoupleStatsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        couple = user_couple_queryset(request.user).first()
        if couple is None:
            return Response(
                {"detail": "Couple not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        today = date.today()
        start = couple.date_of_start
        days_together = (today - start).days

        anniversaries = []
        for years in (1, 2, 3):
            anniversary = start.replace(year=start.year + years)
            anniversaries.append({
                "year": years,
                "date": anniversary,
                "days_until": (anniversary - today).days,
            })

        return Response({
            "couple_id": couple.couple_id,
            "date_of_start": start,
            "days_together": days_together,
            "anniversaries": anniversaries,
        })
