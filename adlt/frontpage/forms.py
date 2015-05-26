import re

from django import forms
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

import adlt.core.models as core_models
import adlt.common.widgets as common_widgets


class ModelTypeaheadField(forms.ModelChoiceField):
    widget = common_widgets.TypeaheadWidget(reverse_lazy('agent-list-json'))

    def prepare_value(self, value):
        if isinstance(value, models.Model):
            return value
        elif value:
            return self.queryset.get(pk=value)
        else:
            return None


class ProjectForm(forms.ModelForm):
    agent = ModelTypeaheadField(
        core_models.Agent.objects.all(), label=_('Organizacija/Asmuo'), required=True,
        help_text=_(
            'Organizacija arba individualus asmuo vykdantis arba planuojantis vykdyti projektą. Pasirinkite esamą '
            'iš sąrašo arba įveskite naują organizacijos pavadinimą arba individualaus asmens vardą.'
        ),
    )

    class Meta:
        model = core_models.Project
        fields = ('title', 'agent', 'description', 'datasets_links')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
            'datasets': forms.Textarea(attrs={'rows': 5}),
        }
        help_texts = {
            'description': _(
                "Apibūdinkite projektą. Galite naudoti "
                "[Markdown](http://daringfireball.net/projects/markdown/syntax){:target=_blank} žymes."
            ),
            'datasets_links': _(
                "Pateikite sąrašą nuorodų arba pavadinimų į duomenų šaltinius, kurie yra reikalingi aprašomam "
                "projektui. Kiekvienas duomenų šaltinis turi būti pateiktas naujoje eilutėje. Jei duomenų šaltinis "
                "jau įtrauktas į [atviriduomenys.lt](http://atviriduomenys.lt) svetainę, pateikitę nuorodą iš "
                "[atviriduomenys.lt](http://atviriduomenys.lt) svetainės. Taip pat galite naudoti nuorodas iš "
                "[opendata.gov.lt](http://opendata.gov.lt/) svetainės."
            ),
        }

    def _get_dataset(self, match, link):
        fragment = match.group(0) + '/datasets/'
        spl = link[len(fragment):].strip('/').split('/')
        if len(spl) == 2:
            agent_slug, dataset_slug = spl
            try:
                return core_models.Dataset.objects.get(agent__slug=agent_slug, slug=dataset_slug)
            except core_models.Dataset.DoesNotExist:
                pass

    def clean_datasets_links(self):
        result = []
        invalid_links = []
        value = self.cleaned_data.get('datasets_links', '')
        pattern = r'^https?://(%s)(:\d+)?' % '|'.join(re.escape(x) for x in settings.SERVER_ALIASES)
        for line in map(str.strip, value.splitlines()):
            if not line:
                continue

            dataset = None
            match = re.match(pattern, line)
            if match:
                dataset = self._get_dataset(match, line)
                if dataset is None:
                    invalid_links.append(line)

            result.append((line, dataset))

        if invalid_links:
            raise forms.ValidationError((
                "Sekantys adresai yra klaidingi:\n"
                "\n"
                "- %s\n"
                "\n"
                "Įsitikinkite, kad nuorodos į atviriduomenys.lt svetainę yra veikiančios ir rodo į duomenų šaltinio "
                "puslapį.\n"
            ) % '\n- '.join(invalid_links))
        else:
            return result


class DatasetForm(forms.ModelForm):
    agent = ModelTypeaheadField(core_models.Agent.objects.all(), label=_('Organizacija/Asmuo'), help_text=_(
        "Organizacija arba individualus asmuo teikiantis duomenis. Pasirinkite esamą iš sąrašo arba įveskite "
        "naują organizacijos pavadinimą arba individualaus asmens vardą."
    ))

    class Meta:
        model = core_models.Dataset
        fields = (
            'title', 'agent', 'maturity_level', 'link', 'description',
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
