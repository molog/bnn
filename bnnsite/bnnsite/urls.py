from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bnnsite.views.home', name='home'),
    # url(r'^bnnsite/', include('bnnsite.foo.urls')),
    url(r'^accounts/', include('accounts.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('bnncore.views',
    url(r'^$', 'summary'),
    url(r'^index$', 'summary', name='index'),
    url(r'^summary$', 'summary', name='summary'),
    url(r'^add_slip$', 'add_slip', name='add_slip'),
    url(r'^history', 'history', name='history'),
)
