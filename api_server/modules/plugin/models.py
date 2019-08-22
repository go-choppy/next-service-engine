# -*- coding: utf-8 -*-
"""
    api_server.modules.plugin.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Plugin database models.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

from marshmallow.fields import Field
from api_server.extensions import db
from sqlalchemy_utils.types.choice import ChoiceType


STATUS = [
    ('EXPIRED', 'Expired'),
    ('FINISHED', 'Finished'),
    ('FAILED', 'Failed'),
    ('ACTIVE', 'Active'),
    ('SUBMITTED', 'Submitted')
]


class ChoiceTypeField(Field):
    """A choice type field.
    """
    def _serialize(self, value, attr, obj, **kwargs):
        return value.value


class Service(db.Model):  # noqa
    """
    Service database model.
    """
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    plugin_name = db.Column(db.String(length=250), nullable=False)
    plugin_command = db.Column(db.String(length=255), nullable=False)
    service_uuid = db.Column(db.String(length=64), nullable=False, unique=True, index=True)
    is_server = db.Column(db.Boolean, nullable=False)
    process_id = db.Column(db.String(length=64), nullable=True)
    access_url = db.Column(db.String(length=255), nullable=False)
    proxy_url = db.Column(db.String(length=255), nullable=True)
    workdir = db.Column(db.String(length=255), nullable=True)
    src_code_dir = db.Column(db.String(length=255), nullable=True)
    status = db.Column(ChoiceType(STATUS), default='SUBMITTED', nullable=False)
    message = db.Column(db.TEXT)

    def __repr__(self):
        return 'Service(%r)' % self.id
