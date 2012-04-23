from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('movies.views',
    url(r'^movies/$',              'index',  name='index'),
    url(r'^movies/(?P<slug>.*)/$', 'detail', name='detail'),
)

urlpatterns += patterns('user.view',
    url(r'^$',         direct_to_template, {'template' : 'user/login.html'}),
    url(r'^user/$',    'index',       name='index'),
    url(r'^dbLogin$',  'dbLogin',     name='dbLogin'),
)

urlpatterns += patterns('general.views',
    url(r'^search/$',         login_required(direct_to_template), {'template' : 'general/search.html'}),
    url(r'^simpleSearch/$',   'simpleSearch',     name='simpleSearch'),
    url(r'^esearch/$',        login_required(direct_to_template), {'template' : 'general/extendedSearch.html'}),
    url(r'^extendedSearch/$', 'extendedSearch',   name='extendedSearch'),
)
