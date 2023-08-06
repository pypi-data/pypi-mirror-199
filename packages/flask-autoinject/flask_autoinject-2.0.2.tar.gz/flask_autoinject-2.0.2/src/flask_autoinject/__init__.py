import flask
from .contexts import AutoInjectMiddleware


def init_app(app: flask.Flask):
    """Initialize the Flask context handling."""
    app.wsgi_app = AutoInjectMiddleware(app.wsgi_app)

__version__ = "2.0.2"
