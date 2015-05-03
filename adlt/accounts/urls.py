import importlib

from django.conf.urls import url, include

import allauth.account.views
import allauth.socialaccount.providers as allauth_providers

import adlt.accounts.views as accounts_views



def get_provider_urls(provider):
    try:
        urls = importlib.import_module(provider.package + '.urls')
    except ImportError:
        return []
    else:
        return getattr(urls, 'urlpatterns', [])


urlpatterns = [
    url(r'^login/$', accounts_views.LoginView.as_view(), name='accounts-login'),
    url(r'', include('allauth.socialaccount.urls')),
]

for provider in allauth_providers.registry.get_list():
    urlpatterns += get_provider_urls(provider)
