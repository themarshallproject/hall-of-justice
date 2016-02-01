from django import template
import requests
import re

register = template.Library()
url_page_re = re.compile('(\&)?page=\d+')


@register.simple_tag(name='doctor_filter_link', takes_context=True)
def doctor_filter_link(context, param, value):
    dict_ = context.request.GET.copy()
    dict_.__setitem__('page', str(1))
    dict_.__setitem__(param, value)
    return '?' + dict_.urlencode(safe=[':', '%', ' '])


@register.filter(name='format_data_range')
def format_data_range(value):
    if value == 'Unk':
        return "Unknown"
    try:
        return int(float(value))
    except ValueError:
        return value


@register.filter(name='sort_by_state')
def sort_by_state(queryset):
    return queryset.order_by('states')


@register.simple_tag(name='pagination_url_doctor', takes_context=True)
def pagination_url_doctor(context, page):
    dict_ = context.request.GET.copy()
    dict_.__setitem__('page', str(page))
    return '?' + dict_.urlencode()