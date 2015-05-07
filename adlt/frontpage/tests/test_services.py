import django.test

import adlt.core.models as core_models
import adlt.core.factories as core_factories
import adlt.frontpage.services as frontpage_services


class ServiceTests(django.test.TransactionTestCase):
    def create(self, data):
        project_agent = core_factories.AgentFactory(title='Project agent')

        for agent, (dataset, stars, dataset_likes), (project, project_likes) in data:
            try:
                agent = core_models.Agent.objects.get(title=agent)
            except core_models.Agent.DoesNotExist:
                agent = core_factories.AgentFactory(title=agent)

            try:
                dataset = core_models.Dataset.objects.get(title=dataset)
            except core_models.Dataset.DoesNotExist:
                dataset = core_factories.DatasetFactory(
                    title=dataset, agent=agent, maturity_level=stars, likes=dataset_likes,
                )
            else:
                self.assertEqual(dataset.agent_id, agent.pk)
                self.assertEqual(dataset.maturity_level, stars)
                self.assertEqual(dataset.likes, dataset_likes)

            if project != 'NN':
                try:
                    project = core_models.Project.objects.get(title=project)
                except core_models.Project.DoesNotExist:
                    project = core_factories.ProjectFactory(title=project, agent=project_agent, likes=project_likes)
                else:
                    self.assertEqual(project.agent_id, project_agent.pk)
                    self.assertEqual(project.likes, project_likes)

                project.datasets.add(dataset)

    # pylint: disable=invalid-name
    def test_orgstats(self):
        self.create([
            # agent   dataset   stars   likes   project   likes
            ('a1',   ('d1',     1,      1),    ('p1',     1)),
            ('a1',   ('d1',     1,      1),    ('p2',     2)),
            ('a1',   ('d1',     1,      1),    ('p3',     4)),
            ('a1',   ('d2',     0,      5),    ('p1',     1)),
            ('a1',   ('d2',     0,      5),    ('p4',     0)),
            ('a1',   ('d2',     0,      5),    ('p5',     5)),
            ('a2',   ('d3',     3,      2),    ('p1',     1)),
            ('a2',   ('d3',     3,      2),    ('p6',     2)),
            ('a2',   ('d4',     1,      1),    ('NN',     0)),
            ('a2',   ('d5',     2,      4),    ('NN',     0)),
            ('a3',   ('d6',     4,      1),    ('NN',     0)),
        ])

        qs = frontpage_services.orgrating()
        result = [(row.likes, row.projects, float(row.stars), row.title) for row in qs]
        self.assertEqual(result, [
            # likes   projects   stars   agent
            (18,      5,         0.5,    'a1'),
            (10,      2,         2.0,    'a2'),
            (1,       0,         4.0,    'a3'),
        ])
