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

@permission_required('movies.watch', login_url="/")
def index(request):
    if request.user.has_perm('movies.allowedRestricted'):
        allMovies = Movie.objects.all().order_by('title')
    else:
        allMovies = Movie.objects.filter(restrictedView=False)

    template = loader.get_template('movie/movie.html')
    context = Context({
        'movies': allMovies,
    })

    return HttpResponse(template.render(context))

def __isSupportedPlaybackFormat(scene):
    if len(scene.sceneRelPath) <= 0: return False
    extension = os.path.splitext(scene.sceneRelPath)[1]

    if extension.lower() in settings.PLAYER_SUPPORTED_FORMATS:
        return True

    return False

def __secondsToDurationString(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    hours   = minutes / 60
    minutes = minutes % 60
    return '%d:%02d:%02d' % (hours, minutes, seconds)

def __enhanceSceneObject(scenes, user):
    durationOfAllScenes = 0
    for scene in scenes:
        if scene.restrictedView and not user.has_perm('movies.allowedRestricted'):
            scene.isRestricted = True
        else:
            scene.isRestricted = False
        scene.genres = Genre.objects.filter(scenes=scene)
        scene.actors = Actor.objects.filter(scenes=scene)
        scene.supportedFormat = __isSupportedPlaybackFormat(scene)
        durationOfAllScenes += scene.duration
    return scenes, durationOfAllScenes

@permission_required('movies.watch', login_url="/")
def detail(request, slug):
    user = request.user
    movie = get_object_or_404(Movie, slug=slug)
    if movie.restrictedView and not user.has_perm('movies.allowedRestricted'):
        return render_to_response('movie/restricted.html')

    directors = Director.objects.filter(movies=movie)

    scenes = Scene.objects.filter(movie=movie)
    scenes, durationInSeconds = __enhanceSceneObject(scenes, user)

    movie.directors = directors
    movie.studio = "STUDIOTODO"
    movie.actors = Actor.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.genres = Genre.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.duration = __secondsToDurationString(durationInSeconds)

    context = Context({
        'movie'  : movie,
        'scenes' : scenes,
        'mediaBasePath' : settings.MOVIE_BASE_DIR
    })

    return render_to_response('movie/detail.html', context)

@permission_required('movies.watch', login_url="/")
def sceneList(request):
    user = request.user

    if user.has_perm('movies.allowedRestricted'):
        allScenes = Scene.objects.all().order_by('title')
    else:
        allScenes = Scene.objects.filter(restrictedView=False)

    allScenes, durationInSeconds = __enhanceSceneObject(allScenes, user)

    context = Context({
        'scenes': allScenes,
    })

    return render_to_response('movie/sceneList.html', context)

@permission_required('movies.watch', login_url="/")
def sceneDetail(request, sha256):
    print sha256
    # get slug of movie of given scenes sha256
    slug = "foo"

    return detail(request, slug)
