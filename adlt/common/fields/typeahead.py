from django import forms
from django.db import models
from django.core.urlresolvers import reverse_lazy


class TypeaheadWidget(forms.TextInput):
    def __init__(self, source_url, attrs=None):
        super().__init__(attrs)
        self.source_url = source_url

    def _get_value_and_label(self, value):
        if isinstance(value, models.Model):
            return value.pk, str(value)
        elif value:
            return value, value
        else:
            return '', ''

    def render(self, name, value, attrs=None):
        value, label = self._get_value_and_label(value)
        attrs = attrs or {}
        attrs['id'] = 'id_' + name + '_typeahead'
        attrs['class'] = ' '.join([self.attrs.get('class', ''), attrs.get('class', ''), 'typeahead'])
        attrs['data-source'] = self.source_url
        attrs['data-input'] = 'id_' + name
        return (
            super().render(name + '_typeahead', label, attrs) +
            '<input type="hidden" id="%s" name="%s" value="%s">' % (attrs['data-input'], name, value)
        )


class ModelTypeaheadField(forms.ModelChoiceField):
    widget = TypeaheadWidget(reverse_lazy('agent-list-json'))

    def prepare_value(self, value):
        if isinstance(value, models.Model):
            return value
        elif value:
            return self.queryset.get(pk=value)
        else:
            return None
