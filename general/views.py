from django.http import HttpResponse
from movies.models import Movie, Scene
from django.template import RequestContext, loader
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from actors.models import Actor
from genres.models import Genre

@permission_required('movies.watch', login_url="/")
def simpleSearch(request):
    searchTerm = request.POST['searchTerm']
    print searchTerm
    searchedMovies = Movie.objects.filter(Q(title__contains=searchTerm) | Q(description__contains=searchTerm))
    #TODO search also in genres scenes.title and actors and accumulate the movies
    template = loader.get_template('movie/movieList.html')
    context = RequestContext(request, {
        'movies': searchedMovies,
    })
    return HttpResponse(template.render(context))

@permission_required('movies.watch', login_url="/")
def extendedSearch(request):
    title = request.POST['title']
    actor = request.POST['actor']
    genre = request.POST['genre']
    print title, actor, genre
    titleMovies = Movie.objects.filter(Q(title__contains=title))
    #TODO search also in genres and actors and accumulate the movies
    template = loader.get_template('movie/movieList.html')
    context = RequestContext(request, {
        'movies': titleMovies,
    })
    return HttpResponse(template.render(context))

@login_required(login_url="/")
def eSearchView(request):
    template = loader.get_template('general/extendedSearch.html')
    context = RequestContext(request, {
        'actors': Actor.objects.all(),
        'genres': Genre.objects.all(),
    })
    return HttpResponse(template.render(context))
