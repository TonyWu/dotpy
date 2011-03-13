from django.conf.urls.defaults import *

urlpatterns = patterns('dotpy.users.views',
    url(r'^signup/$', 'signup', name='user-signup'),
    url(r'^confirm/(?P<code>\w+)/$', 'confirm_signup', name='user-confirm-signup'),
    url(r'^signin/$', 'signin', name='user-signin'),
    url(r'^signout/$', 'signout', name='user-signout'),
    url(r'^forgot-password/$', 'forgot_password', name='user-forgot-password'),
    url(r'^reset-password/(?P<code>\w+)/$', 'reset_password', name='user-reset-password'),
    url(r'^account/$', 'my_account', name='user-account'),

)
