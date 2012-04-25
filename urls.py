from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('movies.views',
    url(r'^movies/$',                'index',  name='movie_index'),
    url(r'^movies/(?P<slug>.*)/$',   'detail', name='detail'),
    url(r'^scenes/$',                'sceneList',  name='sceneList'),
    url(r'^scenes/(?P<sha256>.*)/$', 'sceneDetail', name='sceneDetail'),
)

urlpatterns += patterns('user.view',
    url(r'^$',         direct_to_template, {'template' : 'user/login.html'}),
    url(r'^user/$',    'index',       name='user_index'),
    url(r'^dbLogin$',  'dbLogin',     name='dbLogin'),
)

urlpatterns += patterns('general.views',
    url(r'^search/$',         login_required(direct_to_template), {'template' : 'general/search.html'}),
    url(r'^simpleSearch/$',   'simpleSearch',     name='simpleSearch'),
    url(r'^esearch/$',        login_required(direct_to_template), {'template' : 'general/extendedSearch.html'}),
    url(r'^extendedSearch/$', 'extendedSearch',   name='extendedSearch'),
)

urlpatterns += patterns('actors.views',
    url(r'^actors/$',                       direct_to_template, {'template' : 'actor/actors.html'}),
    url(r'^actors/actors_(?P<letter>.*)/$', 'actors'),
    url(r'^actors/(?P<slug>.*)/$',          'detail', name='actor_detail'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 'django.views.static.serve', document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, 'django.contrib.staticfiles.views.serve', document_root=settings.STATIC_ROOT)
