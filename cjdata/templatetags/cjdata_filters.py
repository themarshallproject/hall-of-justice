from django import template
import requests
import re

register = template.Library()


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


url_page_re = re.compile('page=\d+')
@register.simple_tag(name='pagination_url_doctor', takes_context=True)
def pagination_url_doctor(context, page):
    full_path = context.request.get_full_path()
    page = 'page=' + str(page)
    if re.search(url_page_re, full_path):
        return re.sub(url_page_re, page, full_path)
    else:
        if not context.request.GET.get('page', False):
            return full_path + '?' + page
        else:
            return full_path + '&' + page


