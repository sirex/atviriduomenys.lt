import django.http
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required

import adlt.core.models as core_models
import adlt.frontpage.services as frontpage_services
import adlt.frontpage.forms as frontpage_forms
import adlt.frontpage.helpers as frontpage_helpers
from adlt.common.helpers import formrenderer


def index(request):
    return render(request, 'frontpage/index.html', {
        'agents': frontpage_services.orgrating(),
    })


def project_list(request):
    return render(request, 'frontpage/project_list.html', {
        'projects': frontpage_services.project_rating(),
    })


def dataset_list(request):
    return render(request, 'frontpage/dataset_list.html', {
        'datasets': frontpage_services.dataset_rating(),
    })


def dataset_details(request, agent_slug, dataset_slug):
    dataset = get_object_or_404(core_models.Dataset, agent__slug=agent_slug, slug=dataset_slug)
    return render(request, 'frontpage/dataset_details.html', {
        'dataset': dataset,
        'projects': dataset.project_set.all(),
        'active_topmenu_item': 'dataset-list',
    })


def project_details(request, agent_slug, project_slug):
    project = get_object_or_404(core_models.Project, agent__slug=agent_slug, slug=project_slug)
    return render(request, 'frontpage/project_details.html', {
        'project': project,
        'datasets': project.datasets.all(),
        'active_topmenu_item': 'project-list',
    })


@login_required
def project_form(request):
    form_title = ugettext('Pateikti naują projektą')

    if request.method == 'POST':
        form, agent = frontpage_helpers.get_agent_form(request.POST, frontpage_forms.ProjectForm)
        if form.is_valid():
            frontpage_helpers.save_project_form(request, form, agent)

            queue = frontpage_services.get_next_from_queue(request.user)
            if queue:
                url, args, kwargs = queue.url
                return django.http.HttpResponseRedirect(reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % queue.pk)
            else:
                return redirect('index')
    else:
        form = frontpage_forms.ProjectForm()

    return render(request, 'frontpage/project_form.html', {
        'form': formrenderer.render(request, form, title=form_title, submit=ugettext('Pateikti')),
    })


@login_required
def dataset_form(request):
    title = ugettext('Pateikti naują duomenų šaltinį')
    submit = ugettext('Pateikti')
    description = ''

    if 'qref' in request.GET:
        queue = get_object_or_404(core_models.Queue, pk=request.GET['qref'], user=request.user, completed=False)
        title = ugettext('Informacija apie duomenų šaltinį')
        description = queue.message
    else:
        queue = None

    if request.method == 'POST':
        form, agent = frontpage_helpers.get_agent_form(request.POST, frontpage_forms.DatasetForm)
        if form.is_valid():
            dataset = frontpage_helpers.save_dataset_form(request, form, agent)

            if queue:
                project = core_models.Project.objects.get(pk=queue.context['project_id'])
                project.datasets.add(dataset)
                queue.completed = True
                queue.save()

            queue = frontpage_services.get_next_from_queue(request.user)
            if queue:
                url, args, kwargs = queue.url
                return django.http.HttpResponseRedirect(reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % queue.pk)
            else:
                return redirect('index')
    else:
        initial = queue.data if queue else {}
        form = frontpage_forms.DatasetForm(initial=initial)

    return render(request, 'frontpage/dataset_form.html', {
        'form': formrenderer.render(request, form, title=title, submit=submit, description=description),
    })
