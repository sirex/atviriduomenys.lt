from django.utils.translation import ugettext

import adlt.core.models as core_models
import adlt.frontpage.forms as frontpage_forms


def get_agent_form(data, FormClass):
    agent = None
    if data.get('agent', '').isdigit():
        form = FormClass(data)
    else:
        data = data.copy()
        agent, data['agent'] = data['agent'], ''
        form = FormClass(data)
        form.fields['agent'].required = False
    return form, agent


def get_dataset_from_link(link):
    if link.startswith('http://') or link.startswith('https://'):
        try:
            return core_models.Dataset.objects.get(link=link)
        except core_models.Dataset.DoesNotExist:
            pass
        return frontpage_forms.Dataset.objects.create(link=link)


def get_dataset_from_title(title):
    if title:
        return core_models.Dataset.objects.create(title=title)


def datasets_from_links(links):
    for link in links:
        dataset = get_dataset_from_link(link) or get_dataset_from_title(link)
        if dataset:
            yield dataset


def create_agent_from_title(request, title):
    return core_models.Agent.objects.create(title=title)


def get_dataset_params(link):
    if link.startswith('http://') or link.startswith('https://'):
        return {'link': link}
    else:
        return {'title': link}


def save_dataset_form(request, form, agent):
    data = form.cleaned_data
    project = form.save(commit=False)
    project.agent = data['agent'] or create_agent_from_title(request, agent)
    project.save()


def save_project_form(request, form, agent):
    data = form.cleaned_data
    project = form.save(commit=False)
    project.agent = data['agent'] or create_agent_from_title(request, agent)
    project.save()

    for link in reversed(data['datasets_links']):
        core_models.Queue.objects.create(
            user=request.user,
            url=['create-dataset', [], {}],
            data=get_dataset_params(link),
            message=ugettext(
                'Prašome pateikti daugiau informacijos apie duomenų šaltinį, kuris buvo priskirtas „%s“ projektui.' % (
                    project.title,
                )
            )
        )
