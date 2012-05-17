import os
from django.template import RequestContext, loader
from django.conf import settings
from movies.models import Movie, Scene
from directors.models import Director
from actors.models import Actor
from genres.models import Genre
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import permission_required

@permission_required('movies.watch', login_url="/")
def index(request):
    if request.user.has_perm('movies.allowedRestricted'):
        allMovies = Movie.objects.all().order_by('title')
    else:
        allMovies = Movie.objects.filter(restrictedView=False)

    template = loader.get_template('movie/movieList.html')
    context = RequestContext(request, {
        'movies': allMovies,
    })

    return HttpResponse(template.render(context))

def __isSupportedPlaybackFormat(scene):
    if len(scene.sceneRelPath) <= 0: return False
    extension = os.path.splitext(scene.sceneRelPath)[1]

    if extension.lower() in settings.PLAYER_SUPPORTED_FORMATS:
        return True

    return False

def __getDurationFromScenes(scenes):
    durationOfAllScenes = 0
    for scene in scenes:
        durationOfAllScenes += scene.duration
    return durationOfAllScenes

@permission_required('movies.watch', login_url="/")
def detail(request, slug):
    user = request.user
    movie = get_object_or_404(Movie, slug=slug)
    if movie.restrictedView and not user.has_perm('movies.allowedRestricted'):
        return render_to_response('movie/restrictedMovie.html')

    directors = Director.objects.filter(movies=movie)

    scenes = Scene.objects.filter(movie=movie).order_by('title')

    movie.directors = directors
    movie.studio = "STUDIOTODO"
    movie.actors = Actor.objects.filter(scenes__in=scenes).distinct()
    movie.genres = Genre.objects.filter(scenes__in=scenes).distinct()
    duration = __getDurationFromScenes(scenes)

    context = RequestContext(request, {
        'movie'  : movie,
        'scenes' : scenes,
        'movieDuration': duration,
        'mediaBasePath' : settings.MOVIE_BASE_DIR
    })

    return render_to_response('movie/movieDetail.html', context)

@permission_required('movies.watch', login_url="/")
def sceneList(request):
    scenes = Scene.objects.all().order_by('title')
    context = RequestContext(request, {
        'scenes': scenes,
    })

    return render_to_response('scene/sceneList.html', context)

@permission_required('movies.watch', login_url="/")
def sceneDetail(request, sha256):
    scene = get_object_or_404(Scene, sha256=sha256)
    context = RequestContext(request, {
        'scene' : scene,
        'mediaBasePath' : settings.MOVIE_BASE_DIR
    })

    return render_to_response('scene/sceneDetail.html', context)
