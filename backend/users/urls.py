from inspect import trace

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, "users")

urlpatterns = [
    path("/", include(router.urls)),
]
