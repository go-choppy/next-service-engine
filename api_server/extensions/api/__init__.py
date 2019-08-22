# -*- coding: utf-8 -*-
"""
    api_server.extensions.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    API extension.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

from copy import deepcopy
from .api import Api
from .namespace import Namespace  # noqa
from .http_exceptions import abort  # noqa


api_v1 = Api(
    version='v1.0',
    title="The API Service for Next Service Engine.",
    description=(
        "This documentation describes the Next Service Engine API."
    ),
)


def init_app(app, **kwargs):
    """API extension initialization point.
    """
    # Prevent config variable modification with runtime changes
    api_v1.authorizations = deepcopy(app.config['AUTHORIZATIONS'])
