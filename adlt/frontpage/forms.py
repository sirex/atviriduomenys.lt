from django import forms
from django.utils.translation import ugettext_lazy as _

import adlt.core.models as core_models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = core_models.Project
        fields = ('title', 'description', 'datasets_links')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
            'datasets': forms.Textarea(attrs={'rows': 5}),
        }
        help_texts = {
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
            'title', 'organization', 'maturity_level', 'link', 'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = (
            core_models.Organization.objects.all()
        )
