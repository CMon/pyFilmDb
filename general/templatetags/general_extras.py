from django import template

register = template.Library()

@register.filter
def setValue(value):
    if value:
        return value
    else:
        return "-"
