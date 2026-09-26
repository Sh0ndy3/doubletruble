from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Auth, User
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserSerializer,
)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Invalid login or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user, backend="users.backends.UserAuthBackend")
        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data,
        })


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not check_password(
            serializer.validated_data["old_password"],
            request.user.auth.password,
        ):
            return Response(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.auth.password = make_password(
            serializer.validated_data["new_password"]
        )
        request.user.auth.save()

        return Response({"message": "Password changed successfully"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("auth").all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.select_related("auth").filter(
            user_id=self.request.user.user_id
        )

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.user_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own account.")
        instance.delete()
