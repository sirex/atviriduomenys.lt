import django_webtest

import django.contrib.auth.models as auth_models

import adlt.core.models as core_models
import adlt.core.factories as core_factories


class ViewTests(django_webtest.WebTest):
    def setUp(self):
        super().setUp()
        self.user = auth_models.User.objects.create_user('u1')

    def test_index(self):
        self.app.get('/', user='u1')

    def test_create_project(self):
        agent = core_factories.AgentFactory(title='Org 1')

        resp = self.app.get('/projects/create/', user='u1')
        resp.form['title'] = 'My project'
        resp.form['agent'] = agent.pk
        resp.form['description'] = 'My project description.'
        resp.form['datasets_links'] = 'http://example.com/'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(list(core_models.Project.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-project', 'My project', 'Org 1'),
        ])

    def test_create_project_and_agent(self):
        resp = self.app.get('/projects/create/', user='u1')
        resp.form['title'] = 'My project'
        resp.form['agent'] = 'New agent'
        resp.form['description'] = 'My project description.'
        resp.form['datasets_links'] = 'http://example.com/'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(list(core_models.Project.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-project', 'My project', 'New agent'),
        ])

    def test_create_dataset(self):
        agent = core_factories.AgentFactory(title='Org 1', individual=False)

        resp = self.app.get('/datasets/create/', user='u1')
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
        core_factories.DatasetFactory(title='My dataset', agent=agent)

        self.app.get('/datasets/org-1/my-dataset/', user='u1')

    def test_dataset_update(self):
        agent = core_factories.AgentFactory(title='Org 1')
        core_factories.DatasetFactory(title='My dataset', agent=agent, user=self.user)

        resp = self.app.get('/datasets/org-1/my-dataset/update/', user='u1')
        resp.form['title'] = 'My dataset (updated)'
        resp.form['agent'] = agent.pk
        resp.form['maturity_level'] = '2'
        resp.form['link'] = 'http://example.com/updated/'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)

        dataset = core_models.Dataset.objects.get(agent__slug='org-1', slug='my-dataset')
        self.assertEqual(dataset.title, 'My dataset (updated)')
        self.assertEqual(dataset.maturity_level, 2)
        self.assertEqual(dataset.link, 'http://example.com/updated/')
