import django.test

import adlt.frontpage.forms as frontpage_forms


class FormTests(django.test.TestCase):
    def test_dataset_links_error(self):
        data = {'datasets_links': 'http://localhost:80/invalid/'}
        form = frontpage_forms.ProjectForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['datasets_links'].errors[0], (
            "Sekantys adresai yra klaidingi:\n"
            "\n"
            '- http://localhost:80/invalid/\n'
            "\n"
            "Įsitikinkite, kad nuorodos į atviriduomenys.lt svetainę yra veikiančios ir rodo į duomenų šaltinio "
            "puslapį.\n"
        ))
