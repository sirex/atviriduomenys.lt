from django.shortcuts import render

from adlt.frontpage import forms


def index(request):
    return render(request, 'frontpage/index.html')


def project_form(request):
    form = forms.ProjectForm()
    return render(request, 'frontpage/project_form.html', {
        'form': form,
    })
