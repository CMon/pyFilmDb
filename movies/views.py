import os
from django.template import Context, loader
from django.conf import settings
from movies.models import Movie, Scene
from directors.models import Director
from actors.models import Actor, Person
from genres.models import Genre
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

@permission_required('movies.watch')
def index(request):
    allMovies = Movie.objects.all().order_by('title')

    tamplate = loader.get_template('movie/movie.html')
    context = Context({
        'movies': allMovies,
    })

    return HttpResponse(tamplate.render(context))

def isSupportedPlaybackFormat(scene):
    if len(scene.sceneRelPath) <= 0: return False
    extension = os.path.splitext(scene.sceneRelPath)[1]

    if extension.lower() in settings.PLAYER_SUPPORTED_FORMATS:
        return True

    return False

@permission_required('movies.watch')
def detail(request, slug):
    user = request.user
    movie = get_object_or_404(Movie, slug=slug)
    if movie.restrictedView and not user.has_perm('movies.allowedRestricted'):
        return render_to_response('movie/restricted.html')

    directors = Director.objects.filter(movies=movie)

    scenes = Scene.objects.filter(movie=movie)
    for scene in scenes:
        if scene.restrictedView and not user.has_perm('movies.allowedRestricted'):
            scene.isRestricted = True
        else:
            scene.isRestricted = False

        scene.genres = Genre.objects.filter(scenes=scene)
        scene.actors = Actor.objects.filter(scenes=scene)
        scene.supportedFormat = isSupportedPlaybackFormat(scene)

    movie.directors = directors
    movie.studio = "STUDIOTODO"
    movie.actors = Actor.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.genres = Genre.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.duration = 666 # TODO: all durations of every scene

    context = Context({
        'movie'  : movie,
        'scenes' : scenes,
        'mediaBasePath' : settings.MOVIE_BASE_DIR
    })

    return render_to_response('movie/detail.html', context)
