"""Gunicorn configuration for development and production."""

import os

bind = "0.0.0.0:8000"
workers = 2

if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    reload = True
    accesslog = "-"
