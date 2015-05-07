from django.shortcuts import render

import adlt.helppages.services as helppages_services


def index(request):
    parts = helppages_services.render('index')
    return render(request, 'helppages/help_page.html', dict(
        parts,
        active_topmenu_item='help-index',
    ))


def help_page(request, path):
    parts = helppages_services.render(path)
    return render(request, 'helppages/help_page.html', dict(
        parts,
        active_topmenu_item='help-index',
    ))
