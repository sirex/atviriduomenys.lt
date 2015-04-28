from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import ugettext

from adlt.common.helpers import formrenderer
from adlt.frontpage import forms


def index(request):
    return render(request, 'frontpage/index.html')


def project_form(request):
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = forms.ProjectForm()

    return render(request, 'frontpage/project_form.html', {
        'form': formrenderer.render(
            request, form,
            title=ugettext('Pateikti naują projektą'),
            submit=ugettext('Pateikti')
        ),
    })


def dataset_form(request):
    if request.method == 'POST':
        form = forms.DatasetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = forms.DatasetForm()

    return render(request, 'frontpage/dataset_form.html', {
        'form': formrenderer.render(
            request, form,
            title=ugettext('Pateikti naują duomenų šaltinį'),
            submit=ugettext('Pateikti')
        ),
    })
