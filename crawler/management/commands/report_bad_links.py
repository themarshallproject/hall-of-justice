from django.core.management.base import BaseCommand, CommandError
from crawler.models import Crawl
import csv


class Command(BaseCommand):
    help = "Report 'bad' urls (HTTP status 400+) for a given crawl"

    def add_arguments(self, parser):
        parser.add_argument('crawl_id', nargs=1, type=int)
        parser.add_argument('--output_file', default=None, dest='output_file')#Dec 1, 2015 - added the ability to export the bad links to a file

    def handle(self, *args, **options):
        crawl_id = options['crawl_id'][0]
        try:
            crawl = Crawl.objects.get(id=crawl_id)
        except Crawl.DoesNotExist:
            raise CommandError('Crawl "{}" does not exist'.format(crawl_id))

        qs = crawl.urlinspection_set.filter(exists=False).order_by('url')

        def inspection_dict(i):
            return {
                'url': i.url,
                'status_code': i.response_meta.get('status_code', None),
                'server': i.response_meta['headers'].get('server', None),
                'content_type': i.response_meta['headers'].get('content-type', None),
                'is_redirect': i.response_meta.get('is_redirect', None),
                'seconds_elapsed': i.response_meta.get('seconds_elapsed', None),
            }

        fieldnames = ('url', 'status_code', 'server', 'content_type', 'is_redirect', 'seconds_elapsed')
        output = (inspection_dict(x) for x in qs)

        if options.get('output_file') is not None: #checks to see if the optional argument is provided
            out_dest = open(options.get('output_file'), 'w') #if the option is provided we write to a file
        else:
            out_dest = self.stdout #else we write to a standard out (console)

        writer = csv.DictWriter(out_dest, fieldnames, quoting=csv.QUOTE_ALL, extrasaction='ignore')
        writer.writeheader()

        for item in output:
            writer.writerow(item)
