from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import logging

@login_required
def index(request):
    user = None
    if request.user.is_authenticated():
        user = request.user

    template = loader.get_template('user/detail.html')
    context = Context({
        'user': user,
    })

    return HttpResponse(template.render(context))

def dbLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    template = loader.get_template('error.html')
    logger = logging.getLogger(__name__)

    if user is not None:
        if user.is_active:
            login(request, user)
            logger.info('User logged in: %s' % username)
            return redirect('/movies')
        else:
            logger.error('User with disabled login(%s) tried to login' % username)
            return HttpResponse(template.render(Context({'disabledAccount' : True})))
    else:
        logger.error('Invalid User(%s) tried to login' % username)
        return HttpResponse(template.render(Context({'invalidAccount' : True})))

@login_required
def dbLogout(request):
    logout()
    print request.user
    return redirect('/')