from celery import shared_task
import requests


def generate_url_info(url, response):
    '''Generate some information about a url and a response'''
    return {
        'url': url,
        'status_code': response.status_code,
        'headers': dict(response.headers),
        'method': response.request.method if response.request else None
    }


@shared_task
def url_options(url):
    response = requests.options(url)
    info = generate_url_info(url, response)
    info['verbs'] = response.headers.get('allow', None)
    return info


@shared_task
def head_url(url):
    response = requests.head(url)
    info = generate_url_info(url, response)
    return info
