from django.conf.urls.defaults import *
from dotpy.lessons import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^e/(\w+)/?$', views.edit),
    (r'^(\w+)/$', views.show),
    (r'^(\w+)/comment/$', views.show_comments),
)
