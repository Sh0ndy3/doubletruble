from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers

from .models import Auth, User


class UserSerializer(serializers.ModelSerializer):
    login = serializers.CharField(required=False, max_length=100, write_only=True)
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "second_name",
            "birth_date",
            "login",
            "password",
        ]
        read_only_fields = ["user_id"]

    def validate_login(self, value):
        query = Auth.objects.filter(login=value)
        if self.instance is not None:
            query = query.exclude(user=self.instance)
        if query.exists():
            raise serializers.ValidationError("This login is already in use.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        login_value = validated_data.pop("login", None)
        user = User.objects.create(**validated_data)

        if not login_value or not password:
            raise serializers.ValidationError(
                {"auth": "login and password are required when creating a user."}
            )

        Auth.objects.create(
            user=user,
            login=login_value,
            password=make_password(password),
        )
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        login_value = validated_data.pop("login", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if password is not None or login_value is not None:
            auth = instance.auth
            if password is not None:
                auth.password = make_password(password)
            if login_value is not None:
                auth.login = login_value
            auth.save()

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["login"] = instance.auth.login
        return data


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
