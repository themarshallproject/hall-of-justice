from django import template
import requests
import re

register = template.Library()
url_page_re = re.compile('(\&)?page=\d+')


def doctor_get_params_func(context, param):
    full_path = context.request.get_full_path()
    if context.request.GET:
        return full_path + '&' + param
    else:
        return full_path + '?' + param


@register.simple_tag(name='doctor_filter_link', takes_context=True)
def doctor_filter_link(context, param):
    full_path = doctor_get_params_func(context, param)
    full_path = re.sub(url_page_re, '', full_path)
    return full_path


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
    full_path = context.request.get_full_path()
    page = 'page=' + str(page)
    if re.search(url_page_re, full_path):
        return re.sub(url_page_re, page, full_path)
    else:
        return doctor_get_params_func(context, page)
