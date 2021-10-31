from django.conf import settings


def get_redirect_path():
    """ Create the payment redirect route for callback"""
    ui_domain = settings.UI_DOMAIN
    ui_route = settings.UI_ROUTE
    return f'{ui_domain}{ui_route}'
