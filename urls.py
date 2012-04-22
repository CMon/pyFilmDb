from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

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
