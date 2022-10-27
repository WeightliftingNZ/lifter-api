"""App configuration."""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """User configuration for this application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
