from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

# Comment the next two lines to disable the admin:
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
    url(r'^$',             direct_to_template, {'template' : 'user/login.html'}),
    url(r'^user/$',        'index',       name='user_index'),
    url(r'^dbLogin$',      'dbLogin',     name='dbLogin'),
    url(r'^user/logout/$', 'dbLogout',    name='dbLogout'),
)

urlpatterns += patterns('general.views',
    url(r'^search/$',         login_required(direct_to_template), {'template' : 'general/simpleSearch.html'}),
    url(r'^simpleSearch/$',   'simpleSearch',     name='simpleSearch'),
    url(r'^esearch/$',        'eSearchView',      name='eSearchView'),
    url(r'^extendedSearch/$', 'extendedSearch',   name='extendedSearch'),
)

urlpatterns += patterns('actors.views',
    url(r'^actors/$',                       direct_to_template, {'template' : 'actor/actorList.html'}, name='actors'),
    url(r'^actors/actors_(?P<letter>.*)/$', 'actors'),
    url(r'^actors/(?P<slug>.*)/$',          'detail', name='actor_detail'),
)

urlpatterns += patterns('genres.views',
    url(r'^genres/$',                       'genres', name='genres'),
    url(r'^genres/(?P<slug>.*)/$',          'detail', name='genre_detail'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 'django.views.static.serve', document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, 'django.contrib.staticfiles.views.serve', document_root=settings.STATIC_ROOT)
