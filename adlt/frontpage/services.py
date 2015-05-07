from django.db.models import Avg, Count

import adlt.core.models as core_models


def orgrating():
    return core_models.Agent.objects.raw('''
    SELECT
        agent.id,
        agent.slug,
        agent.title,
        dataset.stars,
        dataset.likes + COALESCE(project.likes, 0) likes,
        COALESCE(project.projects, 0) projects
    FROM core_agent agent
    JOIN (
        SELECT
            core_dataset.agent_id,
            SUM(core_dataset.likes) likes,
            AVG(core_dataset.maturity_level) stars
        FROM core_dataset
        GROUP BY core_dataset.agent_id
    ) dataset ON dataset.agent_id = agent.id
    LEFT JOIN (
        SELECT
            project.agent_id,
            SUM(project.likes) likes,
            COUNT(project.id) projects
        FROM (
            SELECT DISTINCT
                dataset.agent_id,
                project.id,
                project.likes
            FROM core_dataset dataset
            JOIN core_project_datasets pds ON pds.dataset_id = dataset.id
            JOIN core_project project ON pds.project_id = project.id
        ) project
        GROUP BY project.agent_id
    ) project ON project.agent_id = agent.id
    ORDER BY
        (dataset.likes + COALESCE(project.likes, 0)) DESC,
        COALESCE(project.projects, 0) DESC,
        dataset.stars DESC,
        agent.title
    ''')


def project_rating():
    return (
        core_models.Project.objects.
        values('agent__slug', 'slug', 'title', 'likes').
        annotate(
            stars=Avg('datasets__maturity_level'),
            datasets=Count('datasets'),
        ).
        order_by('-likes', 'title')
    )


def dataset_rating():
    return (
        core_models.Dataset.objects.
        values('agent__slug', 'slug', 'agent__title', 'title', 'likes', 'maturity_level').
        annotate(projects=Count('project')).
        order_by('-likes', '-projects', 'title')
    )


def get_next_from_queue(user):
    return core_models.Queue.objects.filter(user=user, completed=False).order_by('-created').first()
