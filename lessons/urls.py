from django.conf.urls.defaults import *
from dotpy.lessons import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^python/', views.learn_python),
    (r'^django/', views.learn_django),
)
