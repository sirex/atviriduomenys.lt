import django.test

import adlt.core.factories as core_factories
import adlt.frontpage.forms as frontpage_forms


class FormTests(django.test.TestCase):
    def test_success(self):
        agent = core_factories.AgentFactory(title='Agent 1')
        dataset = core_factories.DatasetFactory(title='Dataset 1', agent=agent)

        data = {
            'title': 'Project 1',
            'agent': agent.pk,
            'datasets': (
                'http://localhost:80/datasets/agent-1/dataset-1/\n'
                'http://example.com/lint/to/dataset/\n'
            ),
            'description': 'Project description.',
        }
        form = frontpage_forms.ProjectForm(data)
        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertEqual(form.cleaned_data['datasets'], [
            ('http://localhost:80/datasets/agent-1/dataset-1/', dataset),
            ('http://example.com/lint/to/dataset/', None),
        ])

    def test_dataset_links_error(self):
        data = {'datasets': 'http://localhost:80/invalid/'}
        form = frontpage_forms.ProjectForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['datasets'].errors[0], (
            "Sekantys adresai yra klaidingi:\n"
            "\n"
            '- http://localhost:80/invalid/\n'
            "\n"
            "Įsitikinkite, kad nuorodos į localhost:80 svetainę yra veikiančios ir rodo į duomenų šaltinio "
            "puslapį.\n"
        ))
