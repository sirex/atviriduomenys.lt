from django.conf import settings

import allauth.socialaccount.providers


def get_openid_brands(request):
    brands = {}
    provider = allauth.socialaccount.providers.registry.by_id('openid')
    for brand in provider.get_brands():
        brands['openid.%s' % brand['id']] = {
            'id': brand['id'],
            'name': brand['name'],
            'url': provider.get_login_url(request, openid=brand['openid_url']),
        }
    return brands


def get_other_providers(request, exclude):
    providers = {}
    for provider in allauth.socialaccount.providers.registry.get_list():
        if provider.id in exclude:
            continue
        providers[provider.id] = {
            'id': provider.id,
            'name': provider.name,
            'url': provider.get_login_url(request),
        }
    return providers


def get_auth_providers(request):
    providers = get_openid_brands(request)
    providers.update(get_other_providers(request, exclude={'openid'}))
    for name in settings.SORTED_AUTH_PROVIDERS:
        yield providers[name]
