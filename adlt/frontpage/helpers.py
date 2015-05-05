from django.conf import settings
from django.utils.translation import ugettext

import adlt.core.models as core_models
import adlt.frontpage.forms as frontpage_forms


def get_agent_form(data, FormClass, **kwargs):
    agent = None
    if data.get('agent', '').isdigit():
        form = FormClass(data, **kwargs)
    else:
        data = data.copy()
        agent, data['agent'] = data['agent'], ''
        form = FormClass(data, **kwargs)
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
    return core_models.Agent.objects.create(title=title, user=request.user)


def get_dataset_params(link):
    if link.startswith('http://') or link.startswith('https://'):
        return {'link': link}
    else:
        return {'title': link}


def save_dataset_form(request, form, agent):
    data = form.cleaned_data
    dataset = form.save(commit=False)
    dataset.user = request.user
    dataset.agent = data['agent'] or create_agent_from_title(request, agent)
    dataset.save()
    return dataset


def parse_dataset_links(links):
    prefix = settings.WEBSITE_URL + 'datasets/'
    for link in links:
        dataset = None
        if link.startswith(prefix):
            spl = link[len(prefix):].strip('/').split('/')
            if len(spl) == 2:
                agent_slug, dataset_slug = spl
                try:
                    dataset = core_models.Dataset.objects.get(agent__slug=agent_slug, slug=dataset_slug)
                except core_models.Dataset.DoesNotExist:
                    pass
        yield link, dataset


def update_project_links(links, line, dataset):
    result = []
    for link in links.splitlines():
        link = link.strip()
        if link == line:
            link = settings.WEBSITE_URL + dataset.get_absolute_url().lstrip('/')
        result.append(link + '\n')
    return ''.join(result)


def save_project_form(request, form, agent):
    data = form.cleaned_data
    project = form.save(commit=False)
    project.user = request.user
    project.agent = data['agent'] or create_agent_from_title(request, agent)
    project.datasets_links = ''.join(x + '\n' for x in data['datasets_links'])
    project.save()

    existing_datasets = project.datasets.values_list('pk', flat=True)
    dataset_ids = []
    for link, dataset in parse_dataset_links(reversed(data['datasets_links'])):
        if dataset is None:
            core_models.Queue.objects.create(
                user=request.user,
                url=['create-dataset', [], {}],
                data=get_dataset_params(link),
                context={'project_id': project.pk, 'link': link},
                message=ugettext((
                    "Prašome pateikti daugiau informacijos apie duomenų šaltinį, kuris buvo priskirtas „%s“ "
                    "projektui."
                ) % project.title)
            )
        else:
            dataset_ids.append(dataset.pk)
            if dataset.pk not in existing_datasets:
                project.datasets.add(dataset)

    # Delete datasets that are no longer in dataset links
    for dataset in project.datasets.exclude(id__in=dataset_ids):
        project.datasets.remove(dataset)
