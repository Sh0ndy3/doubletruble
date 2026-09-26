from django.db import models
import uuid


class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="userID"
    )
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Auth(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="userID",
        related_name="auth"
    )
    login = models.CharField(
        max_length=100,
        unique=True,
    )
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.login
