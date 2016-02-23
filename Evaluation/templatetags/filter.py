from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def index(mylist, i):
    """
    Usage: my_list|index:x|index:y

    :param mylist indexable object
    :param i index to access given object
    """
    return mylist[i]


@register.simple_tag
def url_replace(request, field, value):
    """
    Usage: <a href="?{% url_replace request 'param' value %}">

    :param request Request context of this view
    :param field Url field name to modify/add
    :param value Value of the field
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
