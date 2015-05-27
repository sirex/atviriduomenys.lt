from django import forms
from django.utils.translation import ugettext_lazy as _

import adlt.core.models as core_models
from adlt.common.fields import typeahead
from adlt.common.fields import linkref


class ProjectForm(forms.ModelForm):
    agent = typeahead.ModelTypeaheadField(
        core_models.Agent.objects.all(), label=_('Organizacija/Asmuo'), required=True,
        help_text=_(
            'Organizacija arba individualus asmuo vykdantis arba planuojantis vykdyti projektą. Pasirinkite esamą '
            'iš sąrašo arba įveskite naują organizacijos pavadinimą arba individualaus asmens vardą.'
        ),
    )
    datasets = linkref.LinkRefField(
        core_models.Dataset.objects.all(), r'/datasets/(?P<agent__slug>[a-z0-9-]+)/(?P<slug>[a-z0-9-]+)/',
    )

    class Meta:
        model = core_models.Project
        fields = ('title', 'agent', 'description', 'datasets')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
        }
        help_texts = {
            'description': _(
                "Apibūdinkite projektą. Galite naudoti "
                "[Markdown](http://daringfireball.net/projects/markdown/syntax){:target=_blank} žymes."
            ),
            'datasets': _(
                "Pateikite sąrašą nuorodų arba pavadinimų į duomenų šaltinius, kurie yra reikalingi aprašomam "
                "projektui. Kiekvienas duomenų šaltinis turi būti pateiktas naujoje eilutėje. Jei duomenų šaltinis "
                "jau įtrauktas į [atviriduomenys.lt](http://atviriduomenys.lt) svetainę, pateikitę nuorodą iš "
                "[atviriduomenys.lt](http://atviriduomenys.lt) svetainės. Taip pat galite naudoti nuorodas iš "
                "[opendata.gov.lt](http://opendata.gov.lt/) svetainės."
            ),
        }


class DatasetForm(forms.ModelForm):
    agent = typeahead.ModelTypeaheadField(core_models.Agent.objects.all(), label=_('Organizacija/Asmuo'), help_text=_(
        "Organizacija arba individualus asmuo teikiantis duomenis. Pasirinkite esamą iš sąrašo arba įveskite "
        "naują organizacijos pavadinimą arba individualaus asmens vardą."
    ))
    sources = linkref.LinkRefField(
        core_models.Dataset.objects.all(), r'/datasets/(?P<agent__slug>[a-z0-9-]+)/(?P<slug>[a-z0-9-]+)/',
        required=False, label=_("Pirminiai šaltiniai"), help_text=_(
            "Nurodykite pirminius duomenų šaltinius, jei tokių yra, kurių pagrindu buvo sukurtas šis išvestinis "
            "duomenų šaltinis."
        )
    )

    class Meta:
        model = core_models.Dataset
        fields = (
            'title', 'agent', 'maturity_level', 'link', 'sources', 'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
        }
        help_texts = {
            'description': _(
                "Apibūdinkite projektą. Galite naudoti "
                "[Markdown](http://daringfireball.net/projects/markdown/syntax){:target=_blank} žymes."
            ),
        }
