import csv
import itertools
import re
from django.utils.encoding import smart_text
from django.core.exceptions import FieldDoesNotExist


MARKDOWN_LIST_ITEM_REG = r'^(?P<indent>\s*)[\-+*]\s(?P<item>.*)$'


class Echo(object):

    """An object that implements just the write method of the file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def generate_rows(queryset, fieldnames):
    def values_for_fields(object, fieldnames):
        concrete_model = object._meta.concrete_model
        for name in fieldnames:
            try:
                field = concrete_model._meta.get_field(name)
                if field.rel and field.rel.many_to_many:
                    manager = getattr(object, field.name)
                    yield ", ".join(smart_text(related) for related in manager.all())
                else:
                    yield field.value_to_string(object)
            except FieldDoesNotExist:
                pass

    for object in queryset:
        yield list(value for value in values_for_fields(object, fieldnames))


def generate_csv(queryset, fieldnames):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        rows = generate_rows(queryset, fieldnames)
        return itertools.chain((writer.writerow(header) for header in (fieldnames,)),
                               (writer.writerow(row) for row in rows))


def parse_markdown_list(input_string):
    '''Simple markdown list parser that supports single-line list items only.'''
    list_item = re.compile(MARKDOWN_LIST_ITEM_REG)
    for line in input_string.splitlines():
        match = list_item.match(line)
        if match:
            match_dict = match.groupdict()
            indent = len(match_dict['indent'])
            item = match_dict['item'].strip()
            yield indent, item
