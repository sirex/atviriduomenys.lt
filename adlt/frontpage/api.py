from adlt.common.helpers import ajax
import adlt.core.models as core_models


@ajax.request('GET')
def agent_list(request):
    return [
        {
            'pk': agent.pk,
            'title': agent.title,
        }
        for agent in core_models.Agent.objects.all()
    ]
