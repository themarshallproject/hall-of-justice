from django import template

register = template.Library()

@register.filter(name='format_data_range')
def format_data_range(value):
    if value == 'Unk':
        return "Unknown"
    try:
        return int(float(value))
    except ValueError:
        return value