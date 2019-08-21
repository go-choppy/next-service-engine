# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from next_service_engine.plugin import BasePlugin


class DensityPlotPlugin(BasePlugin):
    """
    Density plot plugin for next_service_engine.

    :Example:
    @density-plot()
    """
    plugin_name = 'density-plot'
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    is_server = True

    def __init__(self, *args, **kwargs):
        super(DensityPlotPlugin, self).__init__(*args, **kwargs)

    def check_plugin_args(self, **kwargs):
        pass
