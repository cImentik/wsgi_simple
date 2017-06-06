from urllib.parse import parse_qs

"""
Implemets BaseView class to handle basic operations with environ and start_fn.
"""

ENCODING = "utf8"


class NoTemplateError(Exception):
    pass


class BaseView():

    def __init__(self, environ, start_fn):
        self.environ = environ
        self.start_fn = start_fn
        self.req_get = parse_qs(environ['QUERY_STRING'])
        self.req_post = self.parse_post_qs(environ)

    def parse_post_qs(self, environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        return parse_qs(request_body.decode('utf-8'))

    def get(self):
        pass

    def post(self):
        pass

    def ajax(delf):
        pass

    def response(self):
        """
        Checking environ['REQUEST_METHOD'] dictionary.

        If a request is GET or POST, then "Content-Type" is "text/httml".
        If XMLHttpRequest (ajax), then "application/json".
        Other methods can not be processed, responces
        is "405 Method Not Allowed".
        """
        if self.environ['REQUEST_METHOD'] == 'GET':
            self.start_fn('200 OK', [('Content-Type', 'text/html')])
            yield bytes(self.get(), encoding=ENCODING)
        elif self.environ['REQUEST_METHOD'] == 'POST':
            is_ajax = self.environ.get('HTTP_X_REQUESTED_WITH', None)
            if is_ajax:
                self.start_fn('200 OK', [('Content-Type', 'application/json')])
                yield bytes(self.ajax(), encoding=ENCODING)
            else:
                self.start_fn('200 OK', [('Content-Type', 'text/html')])
                yield bytes(self.post(), encoding=ENCODING)
        else:
            method_not_allowed(self.start_fn)

    def __iter__(self):
        return self.response()


def method_not_allowed(environ, start_fn):
    start_fn('405 Method Not Allowed', [('Content-Type', 'text/plain')])
    return [bytes('405 Method Not Allowed', encoding=ENCODING)]


def not_found(environ, start_fn):
    start_fn('404 Not Found', [('Content-Type', 'text/plain')])
    return [bytes('404 Not Found', encoding=ENCODING)]


def render(template, context={}):
    """
    Loads templates from a file.
    Processes using Template class from base_template
    :template: string - file name to template
    """
    from .base_template import Template
    try:
        with open(template, 'r') as f:
            html = f.read()
            return Template(html).render(**context)
    except OSError as e:
        print(e)
        raise NoTemplateError("No Template!")
