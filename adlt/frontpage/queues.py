import django.http
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.functional import cached_property

import adlt.core.models as core_models
import adlt.formqueue.services as formqueue_services
from adlt.common.helpers import formrenderer


class DatasetQueue(object):
    @classmethod
    def get(cls, request):
        qref = request.GET.get('qref')
        if qref:
            item = get_object_or_404(core_models.Queue, pk=qref, user=request.user, completed=False)
        else:
            item = None
        return cls(request, item)

    def __init__(self, request, item=None):
        self.request = request
        self.item = item
        self.next_item = None

    @cached_property
    def source(self):
        """Return new queue class instance by item's context source.

        Usually queue can be used as target and as source. Target queue is responsible for current view and source for
        processing item.
        """
        if self.item:
            source = self.item.context.get('source', 'project')
            if source == 'dataset':
                QueueClass = DatasetSourceQueue
            elif source == 'project':
                QueueClass = ProjectDatasetQueue
            else:
                raise ValueError("Unknown 'source' value: %s" % source)
        else:
            QueueClass = DatasetQueue

        return QueueClass(self.request, self.item)

    @cached_property
    def is_empty(self):
        self.next_item = formqueue_services.get_next(self.request.user)
        return self.next_item is None

    @cached_property
    def is_full(self):
        return not self.is_empty

    def is_active(self):
        return self.item is not None or self.is_full

    def process(self, dataset):  # pylint: disable=unused-argument
        if self.item:
            self.item.completed = True
            self.item.save()

    def redirect(self):
        if self.is_full:
            url, args, kwargs = self.next_item.url
            redirect_url = reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % self.next_item.pk
            return django.http.HttpResponseRedirect(redirect_url)
        elif self.item:
            return self.complete()

    def initial(self):
        return self.item.data if self.item else {}

    def form(self, form):
        title = ugettext('Pateikti naują duomenų šaltinį')
        submit = ugettext('Pateikti')
        description = ''

        if self.item:
            title = ugettext('Informacija apie duomenų šaltinį')
            description = self.item.message
        return formrenderer.render(self.request, form, title=title, submit=submit, description=description)


class ProjectDatasetQueue(DatasetQueue):
    @cached_property
    def object(self):
        return core_models.Project.objects.get(pk=self.item.context['project_id']) if self.item else None

    def add_from_project(self, project, link, create):
        if link.startswith('http://') or link.startswith('https://'):
            data = {'link': link}
        else:
            data = {'title': link}

        core_models.Queue.objects.create(
            user=self.request.user,
            url=['create-dataset', [], {}],
            data=data,
            context={'project_id': project.pk, 'link': link, 'create': create, 'source': 'project'},
            message=ugettext((
                "Prašome pateikti daugiau informacijos apie duomenų šaltinį, kuris buvo priskirtas „%s“ "
                "projektui."
            ) % project.title)
        )

    def process(self, dataset):
        if self.item:
            self.object.datasets.add(dataset)
            self.object.save()
            super().process(dataset)

    def complete(self):
        if self.object:
            if self.item.context.get('create', True):
                messages.success(self.request, ugettext("Projektas „%s“ sėkmingai sukurtas.") % self.object)
            else:
                messages.success(self.request, ugettext("Projektas „%s“ atnaujintas.") % self.object)
            return redirect(self.object)


class DatasetSourceQueue(DatasetQueue):
    @cached_property
    def object(self):
        return core_models.Dataset.objects.get(pk=self.item.context['dataset_id']) if self.item else None

    def add_from_dataset(self, dataset, link, create):
        if link.startswith('http://') or link.startswith('https://'):
            data = {'link': link}
        else:
            data = {'title': link}

        core_models.Queue.objects.create(
            user=self.request.user,
            url=['create-dataset', [], {}],
            data=data,
            context={'dataset_id': dataset.pk, 'link': link, 'create': create, 'source': 'dataset'},
            message=ugettext((
                "Prašome pateikti daugiau informacijos apie pirminį duomenų šaltinį, kurio pagrindu buvo sukurtas "
                "išvestinis „%s“ duomenų šaltinis."
            ) % dataset.title)
        )

    def process(self, dataset):
        if self.item:
            self.object.sources.add(dataset)
            self.object.save()
            super().process(dataset)

    def complete(self):
        if self.object:
            if self.item.context.get('create', True):
                messages.success(self.request, ugettext("Duomenų šaltinis „%s“ sėkmingai sukurtas.") % self.object)
            else:
                messages.success(self.request, ugettext("Duomenų šaltinis „%s“ atnaujintas.") % self.object)
            return redirect(self.object)
