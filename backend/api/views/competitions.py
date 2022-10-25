"""Viewset for competitions."""

from rest_framework import viewsets

from api.models import Competition
from api.serializers import CompetitionDetailSerializer, CompetitionSerializer
from api.views.pagination import StandardSetPagination

from .filters import CompetitionFilter


class CompetitionViewSet(viewsets.ModelViewSet):
    """The `Competition` views.

    Main URL routing:

    - `/competitions` - provides a paginated list view for competitions.
    - `/competitions/:id` - provides a detail view for a competition.
    - `/competitions/:id/lifts` - provide a list view of lifts for a \
            competition.
    - `/competitions/:competition_id/lifts/:lift_id` - provide a detail view \
            for a lift.

    Extra parameters can be provided:

    - `/competitions?ordering=` - ordering by a field. Current fields to order by \
            are `date` (e.g \
            `/athletes?ordering=-date` will give descending order on \
            `last_name`.
    - `/competitions?search=` - search text on the `name` and `location`.
    - `/competitions?page=` - to select a particular page.
    - `/competitions?date_start_after=YYYY-MM-DD&date_end_before=YYYY-MM-DD` \
            - define limits between dates.
    - `/competitions?date_start_after=&date_start_before=&search=&ordering=` \
            - combining multiple parameters together.

    No authorization required:

    - List
    - Detail

    Authorization required:

    - Create
    - Update (PATCH requests preferred)
    - Delete
    """

    filterset_class = CompetitionFilter
    ordering = ["-date_start"]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        """Queryset for competition."""
        return Competition.objects.all()

    def get_serializer_class(self):
        """Serialize competition.

        Differentiates between the detail view and the list view.
        """
        if self.action == "retrieve":
            return CompetitionDetailSerializer
        return CompetitionSerializer
