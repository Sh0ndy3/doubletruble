from django.db import models
import uuid

class File(models.Model):
    fileid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="fileID"
    )
    couple = models.ForeignKey(
        "couples.Couple",
        on_delete=models.CASCADE,
        related_name="files",
        db_column="coupleID"
    )
    file_name = models.CharField()
    file_type = models.CharField()
    file_URL = models.CharField()
    file_note = models.TextField()
    file_original_name = models.CharField()

    def __str__(self):
        return f"{self.file_original_name} {self.file_type} {self.file_name} {self.file_URL} {self.file_note}"