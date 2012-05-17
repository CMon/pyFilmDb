from django import template

register = template.Library()

def __secondsToDurationString(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    hours   = minutes / 60
    minutes = minutes % 60
    return '%d:%02d:%02d' % (hours, minutes, seconds)

@register.filter
def allowedToView(value, user):
    print value, user
    if user.has_perm('movies.allowedRestricted'):
        return True
    return not value.restrictedView

@register.filter
def durationToString(seconds):
    return __secondsToDurationString(seconds)
