import os
from django.conf import settings
from celery.schedules import crontab

BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_MESSAGE_COMPRESSION = 'gzip'
# CELERY_DISABLE_RATE_LIMITS = True
# Tasks
CELERY_TASK_SERIALIZER = 'json'
# CELERYD_TASK_TIME_LIMIT = 10 * 60
# Results
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost/1')
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = getattr(settings, 'TIME_ZONE', 'UTC')

CELERYBEAT_SCHEDULE = {
    # Updates search index every 2 hours
    'update-search-index': {
        'task': 'cjdata.tasks.update_search_index',
        'schedule': crontab(minute=15, hour='*/2'),
        'kwargs': {'age': 3},
    },
}
