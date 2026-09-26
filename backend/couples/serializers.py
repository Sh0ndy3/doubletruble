from rest_framework import serializers

from .models import Couple


class CoupleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couple
        fields = [
            "couple_id",
            "partner",
            "second_partner",
            "date_of_start",
        ]
        read_only_fields = ["couple_id", "partner", "second_partner"]


class CoupleCreateSerializer(serializers.Serializer):
    second_partner = serializers.UUIDField()
    date_of_start = serializers.DateField()

    def validate_second_partner(self, value):
        from users.models import User

        if not User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value
