from django.conf.urls import patterns, url
from mixer import views

urlpatterns = patterns('',
    url(r'^$', views.rss, name='rss'),
    url(r'^del/(?P<url_id>\d+)$', views.del_url, name='del_url'),
)
