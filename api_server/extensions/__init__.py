# -*- coding: utf-8 -*-
"""
    api_server.extensions
    ~~~~~~~~~~~~~~~~~~~~~

    Extensions provide access to common resources of the application.
    Please, put new extension instantiations and initializations here.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

from flask_caching import Cache
from flask_marshmallow import Marshmallow
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from flask_cors import CORS
from .flask_sqlalchemy import SQLAlchemy
from .logging import Logging
from . import api

logging = Logging()
cross_origin_resource_sharing = CORS()
force_auto_coercion()
force_instant_defaults()
db = SQLAlchemy()
marshmallow = Marshmallow()
cache = Cache()


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
        logging,
        db,
        marshmallow,
        cross_origin_resource_sharing,
        cache,
        api,
    ):
        extension.init_app(app)
