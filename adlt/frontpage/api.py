from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import F

from adlt.common.helpers import ajax
import adlt.core.models as core_models


@ajax.request('GET')
def agent_list(request):  # pylint: disable=unused-argument
    return [
        {
            'pk': agent.pk,
            'title': agent.title,
        }
        for agent in core_models.Agent.objects.all()
    ]


@login_required
@ajax.request('GET')
def like_toggle(request, object_type, object_id):
    object_types = {
        'dataset': core_models.Dataset,
        'project': core_models.Project,
    }

    if object_type not in object_types:
        raise Http404

    qs = core_models.Likes.objects.filter(user=request.user, object_type=object_type, object_id=object_id)
    if qs.exists():
        object_types[object_type].objects.filter(pk=object_id).update(likes=F('likes') - 1)
        qs.delete()
    else:
        object_types[object_type].objects.filter(pk=object_id).update(likes=F('likes') + 1)
        core_models.Likes.objects.create(user=request.user, object_type=object_type, object_id=object_id)

    return {'status': 'ok'}
