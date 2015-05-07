import django_webtest


class ViewTests(django_webtest.WebTest):
    def test_index(self):
        resp = self.app.get('/pagalba/')
        resp.mustcontain('Turinys')
