from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext

from adlt.common.helpers import formrenderer

import adlt.frontpage.services as frontpage_services
import adlt.frontpage.forms as frontpage_forms


def index(request):
    return render(request, 'frontpage/index.html', {
        'organizations': frontpage_services.orgrating(),
    })


def project_form(request):
    if request.method == 'POST':
        form = frontpage_forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = frontpage_forms.ProjectForm()

    return render(request, 'frontpage/project_form.html', {
        'form': formrenderer.render(
            request, form,
            title=ugettext('Pateikti naują projektą'),
            submit=ugettext('Pateikti')
        ),
    })


def dataset_form(request):
    if request.method == 'POST':
        form = frontpage_forms.DatasetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = frontpage_forms.DatasetForm()

    return render(request, 'frontpage/dataset_form.html', {
        'form': formrenderer.render(
            request, form,
            title=ugettext('Pateikti naują duomenų šaltinį'),
            submit=ugettext('Pateikti')
        ),
    })
