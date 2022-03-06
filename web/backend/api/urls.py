from django.urls import include, path
from rest_framework_nested import routers

from api.views import AthleteViewSet, CompetitionViewSet, SessionViewSet, LifterViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"athletes", AthleteViewSet, "athletes")
router.register(r"competitions", CompetitionViewSet, "competitions")


athletes_router = routers.NestedDefaultRouter(router, r"athletes", lookup="athlete")
athletes_router.register(r"lifters", LifterViewSet, basename="athelete-lifters")

competitions_router = routers.NestedDefaultRouter(
    router, r"competitions", lookup="competition"
)
competitions_router.register(
    r"sessions", SessionViewSet, basename="competition-sessions"
)

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
    path("", include(competitions_router.urls)),
    path("", include(athletes_router.urls)),
]
