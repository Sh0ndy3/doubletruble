from rest_framework import serializers

from .models import List, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ["id"]


class ListSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ["list_id", "couple", "options"]
        read_only_fields = ["list_id", "options"]
