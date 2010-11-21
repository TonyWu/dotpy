from django.conf.urls.defaults import *
from dotpy.lessons import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^python$', views.learn_python, {'title_slug': None}),
    (r'^django$', views.learn_django, {'title_slug': None}),
    (r'^python/(\d+(?:\.\d+){0,3})$', views.learn_python),
    (r'^django/(\d+(?:\.\d+){0,3})$', views.learn_django),
)
