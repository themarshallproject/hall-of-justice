import csv
import itertools


class Echo(object):

    """An object that implements just the write method of the file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def generate_rows(queryset, fieldnames):
    for object in queryset:
        yield list(getattr(object, f, None) for f in fieldnames)


def generate_csv(queryset, fieldnames):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        rows = generate_rows(queryset, fieldnames)
        return itertools.chain((writer.writerow(header) for header in (fieldnames,)),
                               (writer.writerow(row) for row in rows))
