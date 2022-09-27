"""API urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import (
    AthleteViewSet,
    CompetitionViewSet,
    LiftViewSet,
    SearchAPIView,
)

router = DefaultRouter(trailing_slash=False)
# /lifts
# TODO allow searchability among lifts

# /athletes/<athlete pk>
router.register(r"athletes", AthleteViewSet, "athletes")
# /competitions/<competition pk>
router.register(r"competitions", CompetitionViewSet, "competitions")

competitions_router = NestedDefaultRouter(
    router, r"competitions", lookup="competitions"
)
# /competitions/<competition pk>/lifts/<lift pk>
competitions_router.register(
    r"lifts", LiftViewSet, basename="competition-lifts"
)

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    # path("auth/registration/", include("dj_rest_auth.registration.urls")), # block registration for now
    path("", include(router.urls)),
    path("", include(competitions_router.urls)),
    path("search", SearchAPIView.as_view(), name="search"),
]
