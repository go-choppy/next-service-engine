# -*- coding: utf-8 -*-
"""
    api_server.modules.plugin.parameters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Input arguments (Parameters) for Workflow resources RESTful API.

    :copyright: © 2019 by the Choppy team.
    :license: AGPL, see LICENSE.md for more details.
"""

from flask_restplus import reqparse, inputs


# Service
service_get_args = reqparse.RequestParser()
service_get_args.add_argument('page', type=int, required=False, default=1)
service_get_args.add_argument('per_page', type=int, required=False,
                              choices=[5, 10, 20, 30, 40, 50], default=10)
service_get_args.add_argument('status', type=str, required=False,
                              choices=['SUBMITTED', 'FINISHED', 'EXPIRED', 'FAILED', 'ACTIVE'])
service_get_args.add_argument('service_uuid', type=str, required=False)
service_get_args.add_argument('is_server', type=inputs.boolean, default=None,
                              help='Show service that is server.')


# Plugin
plugin_get_args = reqparse.RequestParser()
plugin_get_args.add_argument('show_details', type=inputs.boolean, default=False,
                             help='Show plugin details.')


plugin_post_args = reqparse.RequestParser()
plugin_post_args.add_argument('plugin_name', type=str, required=True, help='Plugin name.')
plugin_post_args.add_argument('plugin_args', type=dict, required=True, help='Plugin keyword arguments.')
