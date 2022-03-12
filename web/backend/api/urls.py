from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import (
    AthleteViewSet,
    CompetitionViewSet,
    LiftViewSet,
)

# /competitons/<competition pk>/lift/<lifts pk>
router = DefaultRouter(trailing_slash=False)
router.register(r"athletes", AthleteViewSet, "athletes")
router.register(r"competitions", CompetitionViewSet, "competitions")
competitions_router = NestedDefaultRouter(
    router, r"competitions", lookup="competitions"
)
competitions_router.register(r"lift", LiftViewSet, basename="competitions-lift")

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
    path("", include(competitions_router.urls)),
]
