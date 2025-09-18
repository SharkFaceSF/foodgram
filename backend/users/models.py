from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .constants import (USER_EMAIL_MAX_LENGTH, USER_NAME_MAX_LENGTH,
                        USER_USERNAME_MAX_LENGTH)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=USER_EMAIL_MAX_LENGTH,
    )
    username = models.CharField(
        unique=True,
        max_length=USER_USERNAME_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Недопустимый формат имени пользователя.',
                code='invalid_username'
            )
        ],
    )
    first_name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    avatar = models.ImageField(
        upload_to="users/avatars/",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["username"]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        unique_together = ["user", "author"]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="запрет_подписки_на_себя",
            ),
        ]
