"""Context handler for Flask."""
from autoinject import injector


class AutoInjectMiddleware:

    def __init__(self, wsgi_app_callback):
        self._app_call = wsgi_app_callback

    @injector.with_contextvars()
    def wsgi_app(self, *args, **kwargs):
        self._app_call(*args, **kwargs)
