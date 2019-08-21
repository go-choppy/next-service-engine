# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from next_service_engine.plugin import BasePlugin


class HeatmapRPlugin(BasePlugin):
    """
    Heatmap plugin for next_service_engine.

    :Example:
    @heatmap-r()
    """
    plugin_name = 'heatmap-r'
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    is_server = True

    def __init__(self, *args, **kwargs):
        super(HeatmapRPlugin, self).__init__(*args, **kwargs)

    def check_plugin_args(self, **kwargs):
        pass
