from django.conf.urls import url

from adlt.frontpage import views

slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.project_list, name='project-list'),
    url(r'^datasets/$', views.dataset_list, name='dataset-list'),
    url(r'^projects/create/$', views.project_form, name='create-project'),
    url(r'^datasets/create/$', views.dataset_form, name='create-dataset'),
    url(r'^datasets/(?P<agent_slug>%s)/(?P<dataset_slug>%s)/$' % (slug, slug), views.dataset_details, name='dataset-details'),
]
