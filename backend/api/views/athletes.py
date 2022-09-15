from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
)
from hashid_field import Hashid
from rest_framework import permissions, viewsets

from api.models import Athlete
from api.serializers import AthleteDetailSerializer, AthleteSerializer
from api.views.pagination import StandardSetPagination

from .filters import AthleteFilter


@extend_schema_view(
    list=extend_schema(
        examples=[
            OpenApiExample(
                "Response List Athlete Example",
                summary="List Athlete",
                description="Payload response for list of atheletes and paging information.",
                value=[
                    {
                        "reference_id": Hashid(0, min_length=7).hashid,
                        "full_name": "SEKONE-FRASER, Douglas",
                        "first_name": "Douglas",
                        "last_name": "Sekone-Fraser",
                        "yearborn": 1991,
                        "age_categories": {
                            # TODO: validate age
                            "is_youth": False,
                            "is_junior": False,
                            "is_senior": True,
                            "is_master": False,
                        },
                    },
                    {
                        "reference_id": Hashid(1, min_length=7).hashid,
                        "full_name": "TIMAJO, David",
                        "first_name": "David",
                        "last_name": "Timajo",
                        "yearborn": 1993,
                        "age_categories": {
                            "is_youth": False,
                            "is_junior": False,
                            "is_senior": True,
                            "is_master": False,
                        },
                    },
                ],
                request_only=False,
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    retrieve=extend_schema(
        examples=[
            OpenApiExample(
                "Response Detail Athlete Example",
                summary="Detail Athlete",
                description="Payload response for detail of a particular athelete.",
                value=[
                    {
                        "reference_id": Hashid(0, min_length=7).hashid,
                        "full_name": "SEKONE-FRASER, Douglas",
                        "first_name": "Douglas",
                        "last_name": "Sekone-Fraser",
                        "yearborn": 1991,
                        "age_categories": {
                            "is_youth": False,
                            "is_junior": False,
                            "is_senior": True,
                            "is_master": False,
                        },
                    },
                ],
                request_only=False,
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    create=extend_schema(
        examples=[
            OpenApiExample(
                "Request Create Athlete Example",
                summary="Athlete Create",
                description="Payload for creating an athlete.",
                value={
                    "first_name": "Andy",
                    "last_name": "Barakauskas",
                    "yearborn": 1992,
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Response Create Athlete Example",
                summary="Athlete Create",
                description="Payload response for creating an athlete.",
                value={
                    "reference_id": Hashid(3, min_length=7).hashid,
                    "full_name": "BARAKAUSKAS, Andy",
                    "first_name": "Andy",
                    "last_name": "Barakauskas",
                    "yearborn": 1992,
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                request_only=False,
                response_only=True,
                status_codes=["201"],
            ),
        ],
    ),
    partial_update=extend_schema(
        examples=[
            OpenApiExample(
                "Request Update Athlete Example",
                summary="Athlete Update",
                description="Payload for updating an athlete.",
                value={
                    "first_name": "Andrius",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Response Create Athlete Example",
                summary="Athlete Update",
                description="Payload for updating an athlete.",
                value={
                    "reference_id": Hashid(3, min_length=7).hashid,
                    "full_name": "BARAKAUSKAS, Andrius",
                    "first_name": "Andrius",
                    "last_name": "Barakauskas",
                    "yearborn": 1992,
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                request_only=False,
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    update=extend_schema(
        examples=[
            OpenApiExample(
                "Request Update Athlete Example",
                summary="Athlete Update",
                description="Payload for updating an athlete.",
                value={
                    "first_name": "Andrius",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Response Create Athlete Example",
                summary="Athlete Update",
                description="Payload for updating an athlete.",
                value={
                    "reference_id": Hashid(3, min_length=7).hashid,
                    "full_name": "BARAKAUSKAS, Andrius",
                    "first_name": "Andrius",
                    "last_name": "Barakauskas",
                    "yearborn": 1992,
                    "age_categories": {
                        "is_youth": False,
                        "is_junior": False,
                        "is_senior": True,
                        "is_master": False,
                    },
                },
                request_only=False,
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
)
class AthleteViewSet(viewsets.ModelViewSet):
    """
    Athletes
    ========
    This is the Athlete views.

    Pagination has been set to 20.

    Ordering can be set to "last_name" or "first_name". Prepend "-" for descending order.

    No authorization required:

    - List
    - Detail

    Authorization required:

    - Create
    - Update (PATCH requests preferred)
    - Delete

    """

    filterset_class = AthleteFilter
    ordering = ["last_name"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        return Athlete.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AthleteDetailSerializer
        return AthleteSerializer
