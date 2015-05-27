import adlt.core.models as core_models


def get_agent_form(data, FormClass, **kwargs):
    agent = None
    agent_value = data.get('agent', '')
    if not agent_value or agent_value.isdigit():
        form = FormClass(data, **kwargs)
    else:
        data = data.copy()
        agent, data['agent'] = data['agent'], ''
        form = FormClass(data, **kwargs)
        form.fields['agent'].required = False
    return form, agent


def create_agent_from_title(request, title):
    return core_models.Agent.objects.create(title=title, user=request.user)


def save_dataset_form(request, form, agent):
    data = form.cleaned_data
    dataset = form.save(commit=False)
    dataset.user = request.user
    dataset.agent = data['agent'] or create_agent_from_title(request, agent)
    dataset.save()
    return dataset


def save_project_form(request, form, queue, agent):
    create = not form.instance.pk
    data = form.cleaned_data
    project = form.save(commit=False)
    project.user = request.user
    project.agent = data['agent'] or create_agent_from_title(request, agent)
    project.save()

    existing_datasets = project.datasets.values_list('pk', flat=True)
    dataset_ids = []
    for link, dataset in reversed(data['datasets']):
        if dataset is None:
            queue.add_from_project(project, link, create)
        else:
            dataset_ids.append(dataset.pk)
            if dataset.pk not in existing_datasets:
                project.datasets.add(dataset)

    # Delete datasets that are no longer in dataset links
    for dataset in project.datasets.exclude(id__in=dataset_ids):
        project.datasets.remove(dataset)

    return project
