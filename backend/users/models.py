from config.settings.base import HASHID_FIELD_SALT
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from hashid_field import HashidAutoField


class CustomUser(AbstractUser):
    """Custom user model.

    This inherits from Django's AbstractUser

    Fields:
      reference_id (str): This is a custom primary key that is a hash id.
      username (str): This is the username, must be unique to other users.
      name (str): This is the user's name; can be the username as well.
      email (str): This is the email of the user.

    """

    reference_id = HashidAutoField(primary_key=True, salt=f"{HASHID_FIELD_SALT}")
    username = models.CharField(_("username"), unique=True, max_length=25)
    name = models.CharField(_("name"), max_length=155, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.username
