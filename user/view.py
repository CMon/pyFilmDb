from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import logging

@login_required(login_url="/")
def index(request):
    user = None
    if request.user.is_authenticated():
        user = get_user(request)

    template = loader.get_template('user/detail.html')
    context = RequestContext(request, {
        'user':        user,
        'permissions': user.get_all_permissions(),
        'groups':      user.get_group_permissions()
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
            return HttpResponse(template.render(RequestContext(request, {'disabledAccount' : True})))
    else:
        logger.error('Invalid User(%s) tried to login' % username)
        return HttpResponse(template.render(RequestContext(request, {'invalidAccount' : True})))

@login_required(login_url="/")
def dbLogout(request):
    logout(request)
    return redirect('/')
