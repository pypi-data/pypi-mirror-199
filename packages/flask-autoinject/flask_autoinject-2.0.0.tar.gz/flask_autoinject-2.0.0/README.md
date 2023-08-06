# Flask AutoInject

Flask integration to provide separate contexts 
for each request regardless of the underlying 
WSGI handler.

As of version 1.1.0, you MUST use the `init_app()` function
to properly use `autoinject` with Flask contexts. Previously,
the informant was registered automatically. Calling `init_app()` 
now (as of 2.0.0) uses the new contextvars integration in `autoinject`
by wrapping the call to wsgi_app() in an `autoinject.with_contextvars()`
decorator. This ensures that injected functions are cleaned up when the call
to wsgi_app() ends and prevents any ordering problems in terms of the 
teardown functions.

Note that this module does not provide management of autoinjected variables
outside of the context of a call to wsgi_app() (essentially from app config push to 
teardown). Any other management you will need to provide yourself.

```python
import flask
import flask_autoinject

app = flask.Flask(__name__)
flask_autoinject.init_app(app)
```
