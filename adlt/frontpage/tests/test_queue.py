import django_webtest

import django.contrib.auth.models as auth_models

import adlt.core.models as core_models
import adlt.core.factories as core_factories
import adlt.frontpage.services as frontpage_services


class ViewTests(django_webtest.WebTest):
    def test_queue(self):  # pylint: disable=too-many-statements
        def qref():
            queue = frontpage_services.get_next_from_queue(user)
            return queue.pk if queue else None

        user = auth_models.User.objects.create_user('u1')

        # Project form
        resp = self.app.get('/projects/create/', user='u1')
        resp.form['title'] = 'My project'
        resp.form['agent'] = 'Org 1'
        resp.form['description'] = 'My project description.'
        resp.form['datasets'] = (
            'New dataset\n'
            'http://example.com/dataset/1\n'
        )
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(resp.location, 'http://localhost:80/datasets/create/?qref=%d' % qref())
        self.assertEqual(list(core_models.Project.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-project', 'My project', 'Org 1'),
        ])

        project = core_models.Project.objects.get(slug='my-project')
        self.assertEqual(list(project.datasets.values_list('title', flat=True)), [])

        # First dataset form
        resp = resp.follow()
        self.assertEqual(resp.form['title'].value, 'New dataset')
        self.assertEqual(resp.form['link'].value, '')
        resp.form['agent'] = 'Org 2'
        resp.form['maturity_level'] = '3'
        resp.form['link'] = 'http://example.com/dataset/2'
        resp.form['description'] = 'New dataset.'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(resp.location, 'http://localhost:80/datasets/create/?qref=%d' % qref())
        self.assertEqual(list(core_models.Dataset.objects.values_list('slug', 'title', 'agent__title')), [
            ('new-dataset', 'New dataset', 'Org 2'),
        ])

        project = core_models.Project.objects.get(slug='my-project')
        self.assertEqual(list(project.datasets.values_list('title', flat=True)), ['New dataset'])

        # Second dataset form
        resp = resp.follow()
        self.assertEqual(resp.form['title'].value, '')
        self.assertEqual(resp.form['link'].value, 'http://example.com/dataset/1')
        resp.form['title'] = 'Dataset 2'
        resp.form['agent'] = str(core_models.Agent.objects.get(title='Org 2').pk)
        resp.form['maturity_level'] = '3'
        resp.form['description'] = 'Dataset 2.'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(qref(), None)
        self.assertEqual(resp.location, 'http://localhost:80/projects/org-1/my-project/')

        qs = core_models.Dataset.objects.order_by('slug')
        self.assertEqual(list(qs.values_list('slug', 'title', 'agent__title')), [
            ('dataset-2', 'Dataset 2', 'Org 2'),
            ('new-dataset', 'New dataset', 'Org 2'),
        ])

        project = core_models.Project.objects.get(slug='my-project')
        self.assertEqual(list(project.datasets.values_list('title', flat=True)), ['New dataset', 'Dataset 2'])
        self.assertEqual(project.user.username, user.username)

        # Update existing project
        agent = core_factories.AgentFactory(title='Agent 7')
        dataset = core_factories.DatasetFactory(title='Dataset 14', agent=agent)
        resp = self.app.get(project.get_absolute_url() + 'update/', user='u1')
        self.assertEqual(resp.form['datasets'].value, (
            'http://localhost:80/datasets/org-2/new-dataset/\n'
            'http://localhost:80/datasets/org-2/dataset-2/\n'
        ))

        resp.form['title'] = 'My project (updated)'
        resp.form['datasets'] = (
            'http://localhost:80/datasets/org-2/dataset-2/\n'
            'http://localhost:80%s\n' % dataset.get_absolute_url()
        )
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(qref(), None)
        self.assertEqual(resp.location, 'http://localhost:80/projects/org-1/my-project/')

        project = core_models.Project.objects.get(slug='my-project')
        dataset_urls = [ds.get_absolute_url() for ds in project.datasets.all()]
        self.assertEqual(dataset_urls, [
            '/datasets/org-2/dataset-2/',
            dataset.get_absolute_url(),
        ])
