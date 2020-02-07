#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""
    api_server.server
    ~~~~~~~~~~~~~~~~~

    Launch a api server for next_service_engine.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

import sys
import click
import logging
import verboselogs
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from api_server import create_app

logging.setLoggerClass(verboselogs.VerboseLogger)
logger = logging.getLogger(__name__)


flask_app = create_app(static_url_path='')
manager = Manager(flask_app)


class CustomServer(Server):
    def __init__(self, host='127.0.0.1', port=5000, use_debugger=None, use_reloader=None, threaded=False, processes=1, passthrough_errors=False, ssl_crt=None, ssl_key=None, **options):
        return super(CustomServer, self).__init__(host=host, port=port, use_debugger=use_debugger, use_reloader=use_reloader, threaded=threaded, processes=processes, passthrough_errors=passthrough_errors, ssl_crt=ssl_crt, ssl_key=ssl_key, **options)

    def __call__(self, app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors, ssl_crt, ssl_key):
        if app.config.get('ENABLE_SWAGGER'):
            from api_server.helper import register_helper
            register_helper(app)

        return super(CustomServer, self).__call__(app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors, ssl_crt, ssl_key)


manager.add_command('runserver', CustomServer())
manager.add_command('db', MigrateCommand)


@manager.option('-H', '--host', default="localhost", help='Domain or IP Address')
@manager.option('-p', '--port', default=8080, help='Port Number')
@manager.option('-f', '--framework', default='gevent', type=click.Choice(['bjoern', 'gevent']),
                help='Run server with framework.')
def prodserver(host, port, framework):
    """Launch an api server in production."""

    if flask_app.config.get('ENABLE_SWAGGER'):
        from api_server.helper import register_helper
        register_helper(flask_app)

    #
    # TODO: this starts the built-in server, which isn't the most
    # efficient.  We should use something better.
    #
    if framework == "gevent":
        from gevent.pywsgi import WSGIServer
        logger.success("Starting gevent based server")
        logger.success('Running Server: %s:%s' % (host, port))
        svc = WSGIServer((host, port), flask_app)
        svc.serve_forever()


def runserver():
    sys.exit(manager.run())


if __name__ == "__main__":
    sys.exit(manager.run())
