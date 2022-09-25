"""Search viewset."""

from itertools import chain

from rest_framework.generics import ListAPIView

from api.models import Athlete, Competition, Lift
from api.serializers import SearchSerializer

from .pagination import StandardSetPagination


class SearchAPIView(ListAPIView):
    """The search viewset allows search along the `Competition` and `Athlete` models."""

    pagination_class = StandardSetPagination

    def get_queryset(self):

        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            # FIXME: types ignore because mypy says too many args
            qs_chain = chain(
                Athlete.objects.search(query),  # type: ignore
                Competition.objects.search(query),  # type: ignore
                Lift.objects.search(query),
            )

            qs = sorted(
                qs_chain,
                key=lambda instance: instance.rank,
                reverse=True,
            )
            self.count = len(qs)
            return qs
        return Athlete.objects.none()

    def get_serializer_class(self):
        return SearchSerializer
