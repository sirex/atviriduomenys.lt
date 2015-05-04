from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth

import adlt.accounts.helpers.allauth as allauth_helpers


def login(request):
    openid_providers, form = allauth_helpers.get_openid_providers(request)
    if form:
        return allauth_helpers.openid_login(request, form)
    else:
        return render(request, 'accounts/login.html', {
            'auth_providers': allauth_helpers.get_auth_providers(request),
            'openid_providers': openid_providers,
        })


def logout(request):
    auth.logout(request)
    return redirect('index')
