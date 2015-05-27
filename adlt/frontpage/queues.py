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
    def __init__(self, request):
        self.request = request
        self.next_item = None

        qref = request.GET.get('qref')
        if qref:
            self.item = get_object_or_404(core_models.Queue, pk=qref, user=request.user, completed=False)
        else:
            self.item = None

    def add_from_project(self, project, link, create):
        if link.startswith('http://') or link.startswith('https://'):
            data = {'link': link}
        else:
            data = {'title': link}

        core_models.Queue.objects.create(
            user=self.request.user,
            url=['create-dataset', [], {}],
            data=data,
            context={'project_id': project.pk, 'link': link, 'create': create},
            message=ugettext((
                "Prašome pateikti daugiau informacijos apie duomenų šaltinį, kuris buvo priskirtas „%s“ "
                "projektui."
            ) % project.title)
        )

    @cached_property
    def is_empty(self):
        self.next_item = formqueue_services.get_next(self.request.user)
        return self.next_item is None

    @cached_property
    def is_full(self):
        return not self.is_empty

    def is_active(self):
        return self.item is not None or self.is_full

    @cached_property
    def project(self):
        return core_models.Project.objects.get(pk=self.item.context['project_id']) if self.item else None

    def process(self, dataset):
        if self.item:
            self.project.datasets.add(dataset)
            self.project.save()
            self.item.completed = True
            self.item.save()

    def redirect(self):
        if self.is_full:
            url, args, kwargs = self.next_item.url
            redirect_url = reverse(url, args=args, kwargs=kwargs) + '?qref=%d' % self.next_item.pk
            return django.http.HttpResponseRedirect(redirect_url)
        elif self.item:
            return self.complete()

    def complete(self):
        if self.project:
            if self.item.context.get('create', True):
                messages.success(self.request, ugettext("Projektas „%s“ sėkmingai sukurtas.") % self.project)
            else:
                messages.success(self.request, ugettext("Projektas „%s“ atnaujintas.") % self.project)
            return redirect(self.project)

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
