"""Custom managers for Lift model."""

from django.db import models


class LiftManager(models.Manager):
    """Lift Manager for Lift Model."""

    def ordered_filter(self, *args, **kwargs):
        """Order lift by weight category specifics.

        1. Weightclasses
        2. Super-heavies
        3. Female before male
        """
        query = super().filter(*args, **kwargs)

        # order on int values for weight classes (i.e. not string)
        query = sorted(  # type: ignore
            query, key=lambda q: int(q.weight_category[1:].replace("+", ""))
        )
        # ordering super heavies
        query = sorted(query, key=lambda q: "+" in q.weight_category)  # type: ignore
        # order female before male
        query = sorted(query, key=lambda q: q.weight_category[0], reverse=True)  # type: ignore

        return query
