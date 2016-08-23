from __future__ import absolute_import

from pyramid.request import Request
from raven import Client as RavenClient
from raven.utils.wsgi import get_current_url, get_headers, get_environ


def raven_tween_factory(handler, registry):
    client = registry.raven
    exception_filter = registry.tet_raven.exception_filter
    extra_data = registry.tet_raven.extra_data

    def raven_tween(request):
        client.http_context(get_http_context(request))
        try:
            response = handler(request)

        except Exception as e:
            client.extra_context(extra_data(request, e))
            handle_exception(request.environ)
            raise

        finally:
            client.context.clear()

        return response

    def get_http_context(request: Request):
        environ = request.environ
        return dict(method=environ.get('REQUEST_METHOD'),
                    url=get_current_url(environ, strip_querystring=True),
                    query_string=environ.get('QUERY_STRING'),
                    headers=dict(get_headers(environ)),
                    env=dict(get_environ(request.environ)))

    def handle_exception(environ=None):
        return client.captureException()

    return raven_tween


class TetRavenSettings:
    def __init__(self):
        self.exception_filter = lambda request, exception: True
        self.extra_data = lambda request, exception: {}

    def set_exception_filter(self, func) -> None:
        self.exception_filter = func

    def set_extra_data(self, func) -> None:
        self.extra_data = func


def set_raven_exception_filter(config, filter_func):
    tet_raven = config.registry.tet_raven
    tet_raven.set_exception_filter(filter_func)


def set_raven_extra_data(config, extra_data_func):
    tet_raven = config.registry.tet_raven
    tet_raven.set_extra_data(extra_data_func)


def includeme(config, over=None, under=None) -> None:
    settings = config.registry.settings
    if 'raven.dsn' in settings:
        config.registry.raven = RavenClient(settings['raven.dsn'])
        if over is not None:
            config.add_tween('tet_raven.raven_tween_factory', over=over)
        elif under is not None:
            config.add_tween('tet_raven.raven_tween_factory', under=under)
        else:
            config.add_tween('tet_raven.raven_tween_factory', under=(
                'pyramid.tweens.excview_tween_factory',
                'INGRESS'
            ))

    config.registry.tet_raven = TetRavenSettings()
    config.add_directive('set_raven_exception_filter', set_raven_exception_filter)
    config.add_directive('set_raven_extra_data', set_raven_extra_data)
