from django.conf.urls import url

from adlt.helppages import views

urlpatterns = [
    url(r'^$', views.index, name='help-index'),
    url(r'^(?P<path>[a-z0-9/-]+)/$', views.help_page, name='help-page'),
]
