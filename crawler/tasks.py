from celery import shared_task
from celery.utils.log import get_task_logger
import requests
from django.utils import timezone
from django.db import DatabaseError
from django.contrib.contenttypes.models import ContentType
from crawler.models import (URLInspection, RelatedObject)

logger = get_task_logger(__name__)


def generate_url_info(url, response):
    '''Generate some information about a url and a response'''
    return {
        'url': url,
        'status_code': response.status_code,
        'headers': dict(response.headers),
        'method': response.request.method if response.request else None,
        'seconds_elapsed': response.elapsed.total_seconds() if response.elapsed else None
    }


@shared_task
def request_url(url, method='GET', verify_ssl=False):
    '''Request a url. Defaults to not verifying SSL and using the 'GET' http method'''
    response = requests.request(method, url, verify=verify_ssl)
    info = generate_url_info(url, response)

    return info


@shared_task
def request_url_options(url):
    info = request_url(url, method='OPTIONS')
    info['verbs'] = info.headers.get('allow', None)
    return info


@shared_task
def inspect_url(url, method='HEAD', related_object=None):
    logger.info('Inspecting URL: {}'.format(url))
    info = request_url(url, method=method)
    result = info.copy()
    crawl_id = related_object.get('crawl_id', None) if related_object else None
    try:
        inspection = URLInspection.objects.create(url=url,
                                                  response_meta=info,
                                                  crawl_id=crawl_id)
    except DatabaseError as e:
        logger.exception(e)
        return
    status_code = info.get('status_code', None)
    if status_code:
        inspection.exists = True if int(status_code) == 200 else False
        if inspection.exists:
            inspection.last_visited = timezone.now()
    if related_object:
        try:
            app_label = related_object.get('app_label', None)
            model = related_object.get('model', None)
            object_id = related_object.get('id', None)
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            RelatedObject.objects.create(inspection=inspection,
                                         content_type=content_type,
                                         object_id=object_id)
            result['related_object'] = related_object
        except Exception as e:
            logger.exception(e)

    inspection.save()

    result['inspection_id'] = inspection.id

    return result
