from django.conf import settings

def debug(context):
    return {'DEBUG': settings.DEBUG}
