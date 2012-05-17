from django.http import HttpResponse
from movies.models import Scene
from django.template import RequestContext, loader
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from actors.models import Actor
from genres.models import Genre

@permission_required('movies.watch', login_url="/")
def simpleSearch(request):
    searchTerm = request.POST['searchTerm']

    if searchTerm:
        error = None
        #TODO search also in genres and actors and accumulate the movies
        scenes = Scene.objects.filter(Q(title__icontains=searchTerm) | Q(description__icontains=searchTerm))
    else:
        error = "Search Term is empty."
        scenes = None

    template = loader.get_template('scene/sceneList.html')
    context = RequestContext(request, {
        'scenes': scenes,
        'error': error,
    })
    return HttpResponse(template.render(context))

@permission_required('movies.watch', login_url="/")
def extendedSearch(request):
    searchFilter = None
    template = loader.get_template('scene/sceneList.html')

    title = request.POST.get('title', None)
    if title:
        searchFilter = Q(title__icontains=title)
    actor = request.POST.get('actor', None)
    if actor:
        if searchFilter:
            searchFilter = searchFilter & Q(actor__in=actor)
        else:
            searchFilter = Q(actor__in=actor)
    genre = request.POST.get('genre', None)
    if genre:
        if searchFilter:
            searchFilter = searchFilter & Q(genre__in=genre)
        else:
            searchFilter = Q(genre__in=genre)

    if not searchFilter:
        scenes = None
        error = "Invalid search term."
    else:
        error = None
        scenes = Scene.objects.filter(searchFilter).order_by('title')

    context = RequestContext(request, {
        'scenes': scenes,
        'error': error,
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
