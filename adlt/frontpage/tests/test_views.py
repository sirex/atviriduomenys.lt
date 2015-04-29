from django_webtest import WebTest


class ViewTests(WebTest):
    def test_index(self):
        self.app.get('/')
