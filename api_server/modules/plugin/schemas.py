# -*- coding: utf-8 -*-
"""
    api_server.modules.plugin.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    RESTful API Plugin Schemas.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

from api_server.extensions import marshmallow
from api_server.modules.plugin.models import ChoiceTypeField
from .models import Service


class ServiceSchema(marshmallow.ModelSchema):
    """
    Base plugin instance schema exposes only the most general fields.
    """
    status = ChoiceTypeField()

    class Meta:
        model = Service
