from django.db.models import Avg, Count

import adlt.core.models as core_models


def orgrating():
    return (
        core_models.Organization.objects.
        values('title').
        annotate(
            stars=Avg('dataset__maturity_level'),
            usage=Count('dataset__project'),
            projects=Count('dataset__project', distinct=True),
        ).
        order_by('-usage', '-stars', 'title')
    )
