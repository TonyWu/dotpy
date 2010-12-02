from django.conf.urls.defaults import *
from dotpy.lessons import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^(\w+)/(\d+(?:\.\d+){0,3})?$', views.show),
)
