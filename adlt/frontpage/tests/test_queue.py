import django_webtest

import django.contrib.auth.models as auth_models

import adlt.core.models as core_models
import adlt.frontpage.services as frontpage_services


class ViewTests(django_webtest.WebTest):
    def test_queue(self):
        def qref():
            queue = frontpage_services.get_next_from_queue(user)
            return queue.pk if queue else None

        user = auth_models.User.objects.create_user('u1')

        # Project form
        resp = self.app.get('/projects/create/', user='u1')
        resp.form['title'] = 'My project'
        resp.form['agent'] = 'Org 1'
        resp.form['description'] = 'My project description.'
        resp.form['datasets_links'] = (
            'New dataset\n'
            'http://example.com/dataset/1\n'
        )
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(resp.location, 'http://localhost:80/datasets/create/?qref=%d' % qref())
        self.assertEqual(list(core_models.Project.objects.values_list('slug', 'title', 'agent__title')), [
            ('my-project', 'My project', 'Org 1'),
        ])

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
        self.assertEqual(resp.location, 'http://localhost:80/')
        self.assertEqual(list(core_models.Dataset.objects.values_list('slug', 'title', 'agent__title')), [
            ('new-dataset', 'New dataset', 'Org 2'),
            ('dataset-2', 'Dataset 2', 'Org 2'),
        ])
