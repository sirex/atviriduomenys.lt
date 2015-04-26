from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from adlt.core import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Submit'))
