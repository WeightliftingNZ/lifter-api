import os

from django.core.wsgi import get_wsgi_application

settings_files = "config.settings.prod"
if os.getenv("DJANGO_DEVELOPMENT") == "yes":
    settings_files = "config.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_files)

application = get_wsgi_application()
