from django import forms
from django.utils.safestring import mark_safe


class TypeaheadWidget(forms.TextInput):
    def __init__(self, source_url, attrs=None):
        super().__init__(attrs)
        self.source_url = source_url

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = ' '.join([self.attrs.get('class', ''), attrs.get('class', ''), 'typeahead'])
        attrs['data-source'] = self.source_url
        return super().render(name, value, attrs)
