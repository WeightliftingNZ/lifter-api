from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    AthleteViewSet,
    CompetitionViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"athletes", AthleteViewSet, "athletes")
router.register(r"competitions", CompetitionViewSet, "competitions")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
]
