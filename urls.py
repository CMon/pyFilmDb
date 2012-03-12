from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('movies.views',
    url(r'^movies/$',               'index',  name='index'),
    url(r'^movies/(?P<title>.*)/$', 'detail', name='detail'),
)
