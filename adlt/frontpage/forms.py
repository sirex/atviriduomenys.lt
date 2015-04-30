from django import forms
from django.utils.translation import ugettext_lazy as _

import adlt.core.models as core_models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = core_models.Project
        fields = ('title', 'agent', 'description', 'datasets_links')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
            'datasets': forms.Textarea(attrs={'rows': 5}),
        }
        help_texts = {
            'agent': _(
                'Organizacija arba individualus asmuo vykdantys arba planuojantys vykdyti projektą. Pasirinkite esamą '
                'iš sąrašo arba įveskite naują organizacijos pavadinimą arba individualaus asmens vardą.'
            ),
            'description': _(
                "Apibūdinkite projektą. Galite naudoti "
                "[Markdown](http://daringfireball.net/projects/markdown/syntax){:target=_blank} "
                "žymes."
            ),
            'datasets_links': _(
                "Pateikite sąrašą nuorodų arba pavadinimų į duomenų "
                "šaltinius, kurie yra reikalingi aprašomam projektui. "
                "Kiekvienas duomenų šaltinis turi būti pateiktas naujoje "
                "eilutėje. Jei duomenų šaltinis jau įtrauktas į "
                "[atviriduomenys.lt](http://atviriduomenys.lt) svetainę, "
                "pateikitę nuorodą iš "
                "[atviriduomenys.lt](http://atviriduomenys.lt) svetainės. "
                "Taip pat galite naudoti nuorodas iš "
                "[opendata.gov.lt](http://opendata.gov.lt/) svetainės."
            ),
        }


class DatasetForm(forms.ModelForm):
    class Meta:
        model = core_models.Dataset
        fields = (
            'title', 'agent', 'maturity_level', 'link', 'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
        }
        help_texts = {
            'agent': _(
                'Organizacija arba individualus asmuo teikiantis duomenis. Pasirinkite esamą iš sąrašo arba įveskite '
                'naują organizacijos pavadinimą arba individualaus asmens vardą.'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = (
            core_models.Agent.objects.filter(individual=False, active=True)
        )
