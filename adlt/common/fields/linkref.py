import re

from django import forms
from django.conf import settings
from django.db.models import QuerySet

from adlt.common import servername


class LinkRefField(forms.ModelChoiceField):
    widget = forms.Textarea(attrs={'rows': 5})

    def __init__(self, queryset, urlpattern, *args, **kwargs):
        aliases = map(re.escape, settings.SERVER_ALIASES)
        self.root_url_pattern = re.compile(r'^https?://(%s)(:\d+)?' % '|'.join(aliases))
        self.object_url_pattern = re.compile(urlpattern)
        super().__init__(queryset, *args, **kwargs)

    def _get_object_by_link(self, prefix, link):
        path = link[len(prefix):]
        match = self.object_url_pattern.match(path)
        if match:
            try:
                return self.queryset.get(**match.groupdict())
            except self.queryset.model.DoesNotExist:
                pass

    def to_python(self, value):
        result = []
        invalid_links = []
        for line in filter(None, map(str.strip, value.splitlines())):
            dataset = None
            match = self.root_url_pattern.match(line)
            if match:
                dataset = self._get_object_by_link(match.group(0), line)
                if dataset is None:
                    invalid_links.append(line)

            result.append((line, dataset))

        if invalid_links:
            raise forms.ValidationError((
                "Sekantys adresai yra klaidingi:\n"
                "\n"
                "- %s\n"
                "\n"
                "Įsitikinkite, kad nuorodos į %s svetainę yra veikiančios ir rodo į duomenų šaltinio puslapį.\n"
            ) % ('\n- '.join(invalid_links), settings.SERVER_NAME))
        else:
            return result

    def prepare_value(self, value):
        if value and isinstance(value, list) and str(value[0]).isalnum():
            objects = {obj.pk: obj for obj in self.queryset.filter(id__in=value)}
            value = [objects[pk] for pk in map(int, value)]
        if isinstance(value, (list, QuerySet)):
            return ''.join([
                servername.get_website_url(ds.get_absolute_url()) + '\n' for ds in value
            ])
        else:
            return super().prepare_value(value)
