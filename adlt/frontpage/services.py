from django.db.models import Avg, Count

import adlt.core.models as core_models


def orgrating():
    return (
        core_models.Agent.objects.
        values('slug', 'title').
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
        values('agent__slug', 'slug', 'title').
        annotate(
            stars=Avg('datasets__maturity_level'),
            datasets=Count('datasets'),
        ).
        order_by('title')
    )


def dataset_rating():
    return (
        core_models.Dataset.objects.
        values('agent__slug', 'slug', 'title', 'maturity_level').
        annotate(projects=Count('project')).
        order_by('-projects', 'title')
    )


def get_next_from_queue(user):
    return core_models.Queue.objects.filter(user=user, completed=False).order_by('-created').first()
