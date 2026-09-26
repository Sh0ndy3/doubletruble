from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_value = kwargs.get("login", username)
        if not login_value or password is None:
            return None

        User = get_user_model()
        try:
            user = User.objects.select_related("auth").get(
                auth__login=login_value
            )
        except User.DoesNotExist:
            return None

        if check_password(password, user.auth.password):
            return user

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
