#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys


def main():
    """Run administrative tasks."""
    if "DJANGO_DEVELOPMENT" not in os.environ:
        logging.warning(
            "DJANGO_DEVELOPMENT not set, defaulting to production set up"
        )
    settings_file = "config.settings.prod"
    if os.getenv("DJANGO_DEVELOPMENT") == "yes":
        logging.debug("Entering development settings")
        settings_file = "config.settings.dev"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
