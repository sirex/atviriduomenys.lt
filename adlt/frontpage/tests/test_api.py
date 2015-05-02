from django_webtest import WebTest

from adlt.core import models as core_models
from adlt.core import factories as core_factories


class ViewTests(WebTest):
    def test_agent_list(self):
        agent = core_factories.AgentFactory(title='Org 1')
        resp = self.app.get('/agents.json')
        self.assertEqual(resp.json, [{'pk': 1, 'title': 'Org 1'}])
