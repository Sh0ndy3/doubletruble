from django.db import models


class Couple(models.Model):
    couple_id = models.AutoField(
        primary_key=True,
        db_column="coupleID"
    )

    partner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="partner_id",
        related_name="first_partner"
    )

    second_partner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="sPartner_id",
        related_name="second_partner"
    )

    date_of_start = models.DateField(
        db_column="dateOfStart"
    )

    def __str__(self):
        return f"{self.partner} + {self.second_partner}"