# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from next_service_engine.plugin import BasePlugin


class GroupBoxPlotPlugin(BasePlugin):
    """
    Group boxplot plugin for next_service_engine.

    :Example:
    @group-boxplot()
    """
    plugin_name = 'group-boxplot'
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    is_server = True

    def __init__(self, *args, **kwargs):
        super(GroupBoxPlotPlugin, self).__init__(*args, **kwargs)

    def check_plugin_args(self, **kwargs):
        pass
