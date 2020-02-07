# -*- coding: utf-8 -*-
"""
    api_server.modules.plugin.resources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    RESTful API Plugin resources.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

import os
import logging
from flask_restplus import Resource, fields
from flask import current_app, jsonify
from next_service_engine.plugin import get_plugins
from next_service_engine.process_mgmt import create_process_manager
from next_service_engine.service import Service
from api_server.extensions.api import Namespace

from .parameters import plugin_get_args, plugin_post_args, service_get_args
from .models import db, Service as ServiceModel
from .schemas import ServiceSchema


api = Namespace('plugins', description='Plugin related operations')


# Plugin body models
plugin_post_fields = api.model('Resource', {
    'plugin_name': fields.String,
    'plugin_args': fields.Raw
})

logger = logging.getLogger(__name__)


def make_query_dict(status='', service_uuid='', is_server=None):
    query = {}
    if status:
        query.update({
            'status': status
        })

    if service_uuid:
        query.update({
            'service_uuid': service_uuid
        })

    if is_server:
        query.update({
            'is_server': is_server
        })
    return query


@api.route('/services')
class ServicesView(Resource):
    @api.doc(responses={
        200: "Success.",
        400: "Bad request.",
    })
    @api.expect(service_get_args, validate=True)
    def get(self):
        """
        List of services.
        Returns a list of services starting from ``offset`` limited by ``limit``
        parameter.
        """
        args = service_get_args.parse_args()
        total = ServiceModel.query.count()
        query = make_query_dict(args['status'], args['service_uuid'], args['is_server'])

        page = args['page']
        offset = 0 if page <= 0 else page - 1
        per_page = args['per_page']
        queryset = ServiceModel.query.filter_by(**query).offset(offset * per_page).limit(per_page).all()
        service_schema = ServiceSchema(many=True)
        result = service_schema.dump(queryset)

        resp = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "success": True,
            "data": result.data
        }
        return jsonify(resp)

    @api.doc(responses={
        201: "Success.",
        400: "Bad request.",
    })
    @api.doc(body=plugin_post_fields)
    @api.expect(plugin_post_args, validate=True)
    def post(self):
        """Launch a service.
        """
        args = plugin_post_args.parse_args()
        plugin_name = args.plugin_name
        plugin_args = args.plugin_args
        plugin = Service(plugin_name, plugin_args, current_app.config)
        resp = plugin.generate()
        # TODO: Add a asynchronous task to check the status of the plugin instance

        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new plugin instance."
        ):
            success = resp.get('success')
            metadata = resp.get('metadata')
            if success:
                new_service = ServiceModel(**metadata)
                db.session.add(new_service)
                logger.info("Launch %s plugin: %s" % (plugin_name, resp))
                return resp, 201
            else:
                return resp, 500


@api.route('/services/<service_uuid>')
@api.doc(params={'service_uuid': 'Service uuid.'})
class ServiceView(Resource):
    @api.doc(responses={
        200: "Success.",
        400: "Bad requests."
    })
    def get(self, service_uuid):
        result = ServiceModel.query.filter_by(service_uuid=service_uuid).first()
        service_schema = ServiceSchema()
        result = service_schema.dump(result)

        resp = {
            "success": True,
            "data": result.data
        }
        return jsonify(resp)

    @api.doc(responses={
        204: "No content.",
        400: "Bad request.",
    })
    def delete(self, service_uuid):
        """Stop a service.
        """
        from next_service_engine.proxy import delete_service_route

        with api.commit_or_abort(
            db.session,
            default_error_message="Failed to stop a new service."
        ):
            instance = ServiceModel.query.filter_by(service_uuid=service_uuid).first()
            # Delete route & service
            delete_service_route(uuid_as_path=service_uuid)

            # Change service's status
            instance.status = 'FINISHED'

            # Kill process
            process_id = instance.process_id
            static_root = current_app.config.get('STATIC_ROOT')
            src_code_dir = os.path.join(static_root, instance.src_code_dir.strip('/'))
            process = create_process_manager(command_dir=src_code_dir, process_id=process_id)
            process.stop_process()
        return 'No content', 204


@api.route('/')
class PluginsView(Resource):
    @api.doc(responses={
        200: "Success.",
        400: "Bad request.",
    })
    @api.doc(params={'show_details': 'Plugin details'})
    @api.expect(plugin_get_args, validate=True)
    def get(self):
        """Get a set of plugins, filterd by something.
        """
        args = plugin_get_args.parse_args()
        show_details = args.show_details
        installed_plugins = get_plugins()
        if not show_details:
            plugins = list(installed_plugins.keys())
        else:
            # TODO: add more details
            plugins = []
        resp = {
            "message": "Success",
            "data": plugins
        }
        return resp, 200
