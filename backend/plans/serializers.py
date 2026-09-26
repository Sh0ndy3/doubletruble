from rest_framework import serializers

from .models import CalendarPlan, Color, Plan, Repeat


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class RepeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repeat
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ["plan_id"]


class CalendarPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarPlan
        fields = "__all__"
