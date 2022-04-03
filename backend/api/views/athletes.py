from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema_view
from rest_framework import filters, permissions, viewsets

from api.models import Athlete
from api.serializers import AthleteDetailSerializer, AthleteSerializer


@extend_schema_view(exclude_fields=("reference_id", "full_name"))
class AthleteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for athlete
    ===================
    - This contains all the athlete's details
    - Can be used to access all lifts from previous competitions
    """

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]
    ordering = ["last_name"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Athlete.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AthleteDetailSerializer
        return AthleteSerializer
