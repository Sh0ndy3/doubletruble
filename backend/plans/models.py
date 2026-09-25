from django.db import models


class Color(models.Model):
    col_id = models.IntegerField(
        primary_key=True,
        db_column="colID"
    )

    col_text = models.CharField(
        max_length=255,
        db_column="colText"
    )

    def __str__(self):
        return self.col_text


class Repeat(models.Model):
    rep_id = models.IntegerField(
        primary_key=True,
        db_column="repID"
    )

    rep_text = models.CharField(
        max_length=255,
        db_column="repText"
    )

    def __str__(self):
        return self.rep_text


class Plan(models.Model):
    plan_id = models.UUIDField(
        primary_key=True,
        editable=False,
        db_column="planID"
    )

    plan_name = models.TextField(
        db_column="planName"
    )

    deadline = models.DateTimeField(
        db_column="deadline"
    )

    plan_note = models.CharField(
        max_length=255,
        db_column="planNote"
    )

    couple = models.ForeignKey(
        "couples.Couple",
        on_delete=models.CASCADE,
        db_column="coupleID",
        related_name="plans"
    )

    def __str__(self):
        return self.plan_name


class CalendarPlan(models.Model):
    calendar_plan_id = models.IntegerField(
        primary_key=True,
        db_column="calendarPlanID"
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        db_column="planID",
        related_name="calendar_plans"
    )

    date_of_start = models.DateTimeField(
        db_column="dateOfStart"
    )

    date_of_end = models.DateTimeField(
        db_column="dateOfEnd"
    )

    repeat = models.ForeignKey(
        Repeat,
        on_delete=models.SET_NULL,
        null=True,
        db_column="repeat_id",
        related_name="calendar_plans"
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        db_column="color_id",
        related_name="calendar_plans"
    )

    def __str__(self):
        return f"{self.plan} — {self.date_of_start}"