from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField

from config.settings import HASHID_FIELD_SALT


class CustomUser(AbstractUser):

    reference_id = HashidAutoField(
        primary_key=True, salt=f"{HASHID_FIELD_SALT}"
    )
    username = models.CharField(_("username"), unique=True, max_length=25)
    name = models.CharField(_("name"), max_length=155, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.username
