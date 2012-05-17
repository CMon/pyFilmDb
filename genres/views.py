from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from genres.models import Genre
from movies.views import enhanceScenesList

@login_required(login_url="/")
def genres(request):
    genres = Genre.objects.all().order_by('shortDescription')

    context = RequestContext(request, {
        'genres': genres,
    })
    return render_to_response('genre/genreList.html', context)

@login_required(login_url="/")
def detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    scenes = genre.scenes.all().order_by('title')
    scenes, durationInSeconds = enhanceScenesList(scenes, request.user)

    context = RequestContext(request, {
        'genre': genre,
        'scenes': scenes
    })

    return render_to_response('genre/genreDetail.html', context)
