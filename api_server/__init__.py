# -*- coding: utf-8 -*-
"""
    api_server
    ~~~~~~~~~~

    RESTful API Server.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

import os
import sys

from flask import Flask
from flask_migrate import Migrate
from api_server.extensions import db
from werkzeug.contrib.fixers import ProxyFix


CONFIG_NAME_MAPPER = {
    'development': 'api_server.config.DevelopmentConfig',
    'testing': 'api_server.config.TestingConfig',
    'production': 'api_server.config.ProductionConfig',
    'local': 'api_server.local_config.LocalConfig',
}


def create_app(flask_config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    # This is a workaround for Alpine Linux (musl libc) quirk:
    # https://github.com/docker-library/python/issues/211
    import threading
    threading.stack_size(2 * 1024 * 1024)

    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, static_folder=static_folder, **kwargs)

    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'development'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                "FLASK_CONFIG environment variable (\"%s\") and flask_config_name argument "
                "(\"%s\") are both set and are not the same." % (
                    env_flask_config_name,
                    flask_config_name
                )
            )

    try:
        app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])
        app.config.from_envvar('FLASK_CONFIG_FILE')
    except ImportError:
        if flask_config_name == 'local':
            app.logger.error(  # pylint: disable=no-member
                "You have to have `local_config.py` or `local_config/__init__.py` in order to use "
                "the default 'local' Flask Config. Alternatively, you may set `FLASK_CONFIG` "
                "environment variable to one of the following options: development, production, "
                "testing."
            )
            sys.exit(1)
        raise
    except RuntimeError:
        app.logger.warning("You may set `FLASK_CONFIG_FILE` environment variable to a custom config file.")

    if app.config['REVERSE_PROXY_SETUP']:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    from . import extensions
    extensions.init_app(app)

    migrate = Migrate(app, db)  # noqa

    from . import modules
    modules.init_app(app)

    return app
