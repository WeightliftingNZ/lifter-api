from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import AthleteViewSet, CompetitionViewSet, LiftViewSet, SessionViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"athletes", AthleteViewSet, "athletes")
router.register(r"competitions", CompetitionViewSet, "competitions")
# /athletes/<athlete pk>
# /competitions/<competition pk>

competitions_router = NestedDefaultRouter(
    router, r"competitions", lookup="competitions"
)
competitions_router.register(
    r"sessions", SessionViewSet, basename="competition-sessions"
)
# /competitions/<competition pk>/session/<session number>

sessions_router = NestedDefaultRouter(
    competitions_router, r"sessions", lookup="sessions"
)
sessions_router.register(r"lifts", LiftViewSet, basename="session-lifts")
# /competitions/<competition pk>/sessions/<session number>/lifts/<lift pk>

competitions_router.register(
    r"lift", LiftViewSet, basename="competitions-session"
)
urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
    path("", include(competitions_router.urls)),
    path("", include(sessions_router.urls)),
]
