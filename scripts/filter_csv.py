#!/usr/bin/env python3

import os
import sys
import logging
import csv
import argparse
from signal import signal, SIGPIPE, SIG_DFL

logger = logging.getLogger()
signal(SIGPIPE, SIG_DFL)


def unidentified_states(item):
    value = item.get('State', None)
    return (value is None or (len(value) > 2 and value.strip() != "National"))


def no_title(item):
    value = item.get('Title', None)
    return value == '' or value is None


def no_group(item):
    value = item.get('Group name', None)
    return value == '' or value is None


def multiple_categories(item):
    value = item.get('Category', '')
    value_list = value.split(',')
    return (len(value_list) > 1)


def main(args):
    filter_name = getattr(args, 'filter', None)
    filter_func = None
    if filter_name == 'ufo-states':
        filter_func = unidentified_states
    elif filter_name == 'no-title':
        filter_func = no_title
    elif filter_name == 'no-group':
        filter_func = no_group
    elif filter_name == 'multi-cat':
        filter_func = multiple_categories

    reader = csv.DictReader(args.infile)
    fieldnames = reader.fieldnames
    filtered_items = filter(filter_func, reader) if filter_func else (r for r in reader)

    writer = csv.DictWriter(sys.stdout, fieldnames)
    writer.writeheader()
    for item in filtered_items:
        writer.writerow(item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Searches a CSV file for.. stuff')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='Path to the CSV file to search on')
    parser.add_argument('filter', type=str,
                        choices=('ufo-states', 'no-title', 'no-group', 'multi-cat'),
                        help='Specify a predefined filter to run on the CSV')
    args = parser.parse_args()
    main(args)
