from django_webtest import WebTest

from adlt.core import models as core_models
from adlt.core import factories as core_factories


class ViewTests(WebTest):
    def test_index(self):
        self.app.get('/')

    def test_create_project(self):
        agent = core_factories.AgentFactory(title='Org 1')

        resp = self.app.get('/projects/create/')
        resp.form['title'] = 'My project'
        resp.form['agent'] = agent.pk
        resp.form['description'] = 'My project description.'
        resp.form['datasets_links'] = 'http://example.com/'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(list(core_models.Project.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-project', 'My project', 'Org 1'),
        ])

    def test_create_dataset(self):
        agent = core_factories.AgentFactory(title='Org 1', individual=False)

        resp = self.app.get('/datasets/create/')
        resp.form['title'] = 'My dataset'
        resp.form['agent'] = agent.pk
        resp.form['maturity_level'] = '1'
        resp.form['link'] = 'http://example.com/'
        resp.form['description'] = 'My dataset description.'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(list(core_models.Dataset.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-dataset', 'My dataset', 'Org 1'),
        ])


    def test_dataset_details(self):
        agent = core_factories.AgentFactory(title='Org 1')
        dataset = core_factories.DatasetFactory(title='My dataset', agent=agent)

        self.app.get('/datasets/org-1/my-dataset/')
