from django.db import models
import uuid

class Wish(models.Model):
    wish_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="wishID"
    )
    couple = models.ForeignKey(
        "couples.Couple",
        on_delete=models.CASCADE,
        related_name="wishes",
        db_column="coupleID"
    )
    link = models.URLField()
    wish_name = models.TextField()
    price = models.IntegerField()
    wish_note = models.TextField()

    def __str__(self):
        return f"{self.link}, {self.wish_name}, {self.wish_note}, {self.price}"

class WishPhoto(models.Model):
    wish = models.ForeignKey(
        Wish,
        on_delete=models.CASCADE,
        db_column="wishID",
        related_name="photos"
    )
    wish_photo_link = models.TextField(
        db_column="wishPhotoLink",
    )

    def __str__(self):
        return self.wish_photo_link