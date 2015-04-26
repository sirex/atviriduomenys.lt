from django.conf.urls import url

from adlt.frontpage import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/create/$', views.project_form, name='create-project'),
]
