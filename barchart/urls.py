from django.conf.urls import patterns, url

from barchart import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
