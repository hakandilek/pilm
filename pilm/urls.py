from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pilm.views.home', name='home'),
    url(r'^files/$',                           'pilm.views.file_index'),
    url(r'^file/new$',                         'pilm.views.file_create'),
    url(r'^file/edit/(?P<name>[ \S]+)/$',      'pilm.views.file_edit'),
    url(r'^file/delete/(?P<name>[ \S]+)/$',    'pilm.views.file_delete'),
    url(r'^packs/$',                           'pilm.views.pack_index'),
    url(r'^query/(?P<key>\S+)/$',              'pilm.views.query'),
    url(r'^assign/pack:(?P<pack_key>\S+)/movie:(?P<movie_key>\S+)/$', 'pilm.views.assign'),
    url(r'^movies/$',                          'pilm.views.movie_index'),
    url(r'^movie/show/(?P<key>[ \S]+)/$',      'pilm.views.movie_show'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
