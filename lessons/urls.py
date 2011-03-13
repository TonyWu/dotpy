from django.conf.urls.defaults import *

urlpatterns = patterns('dotpy.lessons.views',
    url(r'^$', 'home', name='lessons-home'),
    (r'^e/$', 'edit', {'slug': None}),
    (r'^e/(\w+)/$', 'edit'),
    (r'^(\w+)/$', 'show'),
    (r'^(\w+)/comment/$', 'show_comments'),
)
