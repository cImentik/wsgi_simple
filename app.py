from core.base_views import not_found
from views import HomeView, StatView, ViewView, CommentView
from core.middleware import ExceptionHandlerMiddleware

urls = {
    '/': HomeView,
    '/stat/': StatView,
    '/view/': ViewView,
    '/comment/': CommentView,
}


class Application():

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        handler = self.routes.get(environ.get('PATH_INFO')) or not_found
        return handler(environ, start_response)

app = ExceptionHandlerMiddleware(Application(urls))
