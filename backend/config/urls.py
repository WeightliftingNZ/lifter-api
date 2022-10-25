"""Main URLs."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("administration/", admin.site.urls),
    path("v1/", include("api.urls")),
    path("", RedirectView.as_view(url="/v1", permanent=True), name="index"),
    path("schema/download", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("users", include("users.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
