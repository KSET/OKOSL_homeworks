from django.conf.urls import url

from . import views

app_name = 'fts'
urlpatterns = [
    url(r'^unos/$', views.unos, name='unos'),
    url(r'^(?P<movie_id>[0-9]+)/detail$', views.detail, name='detail'),
    url(r'^pretraga/$', views.pretraga, name='pretraga'),
    url(r'^results/$', views.detail, name='results'),
]

