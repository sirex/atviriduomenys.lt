import django.http
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        'can_update': request.user.is_authenticated() and (request.user.is_superuser or dataset.user == request.user)
    })


def project_details(request, agent_slug, project_slug):
    project = get_object_or_404(core_models.Project, agent__slug=agent_slug, slug=project_slug)
    return render(request, 'frontpage/project_details.html', {
        'project': project,
        'datasets': project.datasets.all(),
        'active_topmenu_item': 'project-list',
        'can_update': request.user.is_authenticated() and (request.user.is_superuser or project.user == request.user)
    })


@login_required
def project_update(request, agent_slug, project_slug):
    if request.user.is_superuser:
        project = get_object_or_404(core_models.Project, agent__slug=agent_slug, slug=project_slug)
    else:
        project = get_object_or_404(core_models.Project, agent__slug=agent_slug, slug=project_slug, user=request.user)

    if request.method == 'POST':
        form, agent = frontpage_helpers.get_agent_form(request.POST, frontpage_forms.ProjectForm, instance=project)
        if form.is_valid():
            frontpage_helpers.save_project_form(request, form, agent)

            queue = frontpage_services.get_next_from_queue(request.user)
            if queue:
                url, args, kwargs = queue.url
                return django.http.HttpResponseRedirect(reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % queue.pk)
            else:
                messages.success(request, ugettext("Projektas „%s“ atnaujintas." % project))
                return redirect(project)
    else:
        form = frontpage_forms.ProjectForm(instance=project)

    return render(request, 'frontpage/project_form.html', {
        'form': formrenderer.render(request, form, title=project.title, submit=ugettext('Pateikti')),
    })


@login_required
def project_form(request):
    form_title = ugettext('Pateikti naują projektą')

    if request.method == 'POST':
        form, agent = frontpage_helpers.get_agent_form(request.POST, frontpage_forms.ProjectForm)
        if form.is_valid():
            project = frontpage_helpers.save_project_form(request, form, agent)

            queue = frontpage_services.get_next_from_queue(request.user)
            if queue:
                url, args, kwargs = queue.url
                return django.http.HttpResponseRedirect(reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % queue.pk)
            else:
                messages.success(request, ugettext("Projektas „%s“ sėkmingai sukurtas." % project))
                return redirect(project)
    else:
        form = frontpage_forms.ProjectForm()

    return render(request, 'frontpage/project_form.html', {
        'form': formrenderer.render(request, form, title=form_title, submit=ugettext('Pateikti')),
    })


@login_required
def dataset_update(request, agent_slug, dataset_slug):
    if request.user.is_superuser:
        dataset = get_object_or_404(core_models.Dataset, agent__slug=agent_slug, slug=dataset_slug)
    else:
        dataset = get_object_or_404(core_models.Dataset, agent__slug=agent_slug, slug=dataset_slug, user=request.user)

    if request.method == 'POST':
        form, agent = frontpage_helpers.get_agent_form(request.POST, frontpage_forms.DatasetForm, instance=dataset)
        if form.is_valid():
            dataset = frontpage_helpers.save_dataset_form(request, form, agent)
            messages.success(request, ugettext("Duomenų šaltinis „%s“ atnaujintas." % dataset))
            return redirect(dataset)
    else:
        form = frontpage_forms.DatasetForm(instance=dataset)

    return render(request, 'frontpage/dataset_form.html', {
        'form': formrenderer.render(request, form, title=dataset.title, submit=ugettext("Pateikti")),
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
                project.save()
                queue.completed = True
                queue.save()

            next_queue = frontpage_services.get_next_from_queue(request.user)
            if next_queue:
                url, args, kwargs = next_queue.url
                redirect_url = reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % next_queue.pk
                return django.http.HttpResponseRedirect(redirect_url)
            elif queue:
                messages.success(request, ugettext("Projektas „%s“ sėkminngai sukurtas." % project))
                return redirect(project)
            else:
                messages.success(request, ugettext("Duomenų šaltinis „%s“ sėkminngai sukurtas." % dataset))
                return redirect(dataset)
    else:
        initial = queue.data if queue else {}
        form = frontpage_forms.DatasetForm(initial=initial)

    return render(request, 'frontpage/dataset_form.html', {
        'form': formrenderer.render(request, form, title=title, submit=submit, description=description),
    })
