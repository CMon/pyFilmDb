from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context
from django.contrib.auth.decorators import login_required
from actors.models import Actor

@login_required(login_url="/")
def actors(request, letter):
    if letter == "All":
        allActors = Actor.objects.all()
    else:
        allActors = Actor.objects.filter(person__firstName__istartswith=letter)

    if not allActors.count():
        allActors = None
    print letter
    print allActors

    context = Context({
        'actors': allActors,
    })
    return render_to_response('actor/actors.html', context)

def detail(request, slug):
    actor = Actor.objects.filter(id=slug)

    context = Context({
        'actor': actor,
        })
    return render_to_response('actor/actorDetail.html', context)
