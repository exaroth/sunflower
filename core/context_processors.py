from django.conf import settings


def additional_info(request):
    return dict(
        SITE_NAME = settings.SITE_NAME,
        DEBUG = settings.DEBUG
    )
