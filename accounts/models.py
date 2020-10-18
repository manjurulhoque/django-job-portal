from typing import List

from django.contrib.auth.models import AbstractUser  # type: ignore
from django.db import models  # type: ignore
from django.utils.translation import ugettext as _

from accounts.managers import UserManager

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_CHOICES = ((GENDER_MALE, _("Male")), (GENDER_FEMALE, _("Female")))


class User(AbstractUser):
    username = None
    role = models.CharField(
        max_length=12,
        error_messages={"required": "Role must be provided"},
        verbose_name=_("Role"),
        help_text=_("User role."),
    )
    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
        verbose_name=_("Gender"),
        help_text=_("User gender."),
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        verbose_name=_("Email"),
        help_text=_("User email, also used as username."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self):
        return self.email

    objects = UserManager()
