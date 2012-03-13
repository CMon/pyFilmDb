from django.template import Context, loader
from movies.models import Movie, Scene
from directors.models import Director
from actors.models import Actor, Person
from genres.models import Genre
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q


#https://docs.djangoproject.com/en/1.3/intro/tutorial03/

def index(request):
    allMovies = Movie.objects.all().order_by('title')

    tamplate = loader.get_template('movie/movie.html')
    context = Context({
        'movies': allMovies,
    })

    return HttpResponse(tamplate.render(context))

def detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    directors = Director.objects.filter(movies=movie)

    scenes = Scene.objects.filter(movie=movie)
    for scene in scenes:
        scene.genres = Genre.objects.filter(scenes=scene)
        scene.actors = Actor.objects.filter(scenes=scene)

    movie.directors = directors
    movie.studio = "STUDIOTODO"
    movie.actors = Actor.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.genres = Genre.objects.filter(Q(scenes__in=scenes) | Q(movies=movie)).distinct()
    movie.duration = 666 # TODO: all durations of every scene

    context = Context({
        'movie'  : movie,
        'scenes' : scenes
    })

    return render_to_response('movie/detail.html', context)
