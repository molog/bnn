from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    # basic
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    
    # set lang
    (r'^set_lang/$', 'set_lang'),
)