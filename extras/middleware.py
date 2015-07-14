from django.conf import settings


def likely_show_toolbar(request):
    """
    Show toolbar as long as request isn't ajax and settings.DEBUG is True
    """
    if request.is_ajax():
        return False

    return bool(settings.DEBUG)
