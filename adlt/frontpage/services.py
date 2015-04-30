from django.db.models import Avg, Count

import adlt.core.models as core_models


def orgrating():
    return (
        core_models.Agent.objects.
        values('title').
        annotate(
            stars=Avg('dataset__maturity_level'),
            usage=Count('dataset__project'),
            projects=Count('dataset__project', distinct=True),
        ).
        exclude(usage=0).
        order_by('-usage', '-stars', 'title')
    )


def project_rating():
    return (
        core_models.Project.objects.
        values('title').
        annotate(
            stars=Avg('datasets__maturity_level'),
            datasets=Count('datasets'),
        ).
        order_by('title')
    )


def dataset_rating():
    return (
        core_models.Dataset.objects.
        values('title').
        annotate(projects=Count('project')).
        order_by('-projects', 'title')
    )
