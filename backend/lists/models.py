from django.db import models
import uuid


class List(models.Model):
    list_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="listID"
    )
    couple = models.ForeignKey(
        "couples.Couple",
        on_delete=models.CASCADE,
        related_name="lists",
        db_column="coupleID"
    )

    def __str__(self):
        return str(self.list_id)


class Option(models.Model):
    option_name = models.CharField(
        max_length=255,
        db_column="optionName",
    )
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE,
        related_name="options",
        db_column="listID"
    )

    def __str__(self):
        return self.option_name
