import django.contrib.auth.models as auth_models
from django_webtest import WebTest

from adlt.core import factories as core_factories


def get(obj):
    return obj._meta.model.objects.get(pk=obj.pk)


class ViewTests(WebTest):
    def test_agent_list(self):
        core_factories.AgentFactory(title='Org 1')
        resp = self.app.get('/agents.json')
        self.assertEqual(resp.json, [{'pk': 1, 'title': 'Org 1'}])

    def test_dataset_like(self):
        auth_models.User.objects.create_user('u1')
        agent = core_factories.AgentFactory(title='Agent 1')
        dataset = core_factories.DatasetFactory(title='Ds 1', agent=agent)
        self.assertEqual(dataset.likes, 0)

        resp = self.app.get('/likes/dataset/%d/like/' % dataset.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'ok'})
        self.assertEqual(get(dataset).likes, 1)

        resp = self.app.get('/likes/dataset/%d/like/' % dataset.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'exists'})
        self.assertEqual(get(dataset).likes, 1)

        resp = self.app.get('/likes/dataset/%d/unlike/' % dataset.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'ok'})
        self.assertEqual(get(dataset).likes, 0)

        resp = self.app.get('/likes/dataset/%d/unlike/' % dataset.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'missing'})
        self.assertEqual(get(dataset).likes, 0)

    def test_project_like(self):
        auth_models.User.objects.create_user('u1')
        agent = core_factories.AgentFactory(title='Agent 1')
        project = core_factories.ProjectFactory(title='Ds 1', agent=agent)
        self.assertEqual(project.likes, 0)

        resp = self.app.get('/likes/project/%d/like/' % project.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'ok'})
        self.assertEqual(get(project).likes, 1)

        resp = self.app.get('/likes/project/%d/like/' % project.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'exists'})
        self.assertEqual(get(project).likes, 1)

        resp = self.app.get('/likes/project/%d/unlike/' % project.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'ok'})
        self.assertEqual(get(project).likes, 0)

        resp = self.app.get('/likes/project/%d/unlike/' % project.pk, user='u1')
        self.assertEqual(resp.json, {'status': 'missing'})
        self.assertEqual(get(project).likes, 0)
