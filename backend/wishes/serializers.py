from rest_framework import serializers

from .models import Wish, WishPhoto


class WishesPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishPhoto
        fields = [
            "id",
            "wish",
            "wish_photo_link",
        ]
        read_only_fields = ["id", "wish"]


class WishesSerializer(serializers.ModelSerializer):
    photos = WishesPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Wish
        fields = [
            "wish_id",
            "couple",
            "link",
            "wish_name",
            "wish_note",
            "price",
            "photos",
        ]
        read_only_fields = ["wish_id", "photos"]
