from django.views.generic.edit import FormView

import allauth.account.views as allauth_views
import allauth.socialaccount.providers.openid.forms as openid_forms

import adlt.accounts.helpers.allauth as allauth_helpers


class LoginView(allauth_views.LoginView):
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['auth_providers'] = allauth_helpers.get_auth_providers(self.request)
        context['form'] = openid_forms.LoginForm()
        return context
