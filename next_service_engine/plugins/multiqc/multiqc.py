# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from next_service_engine.plugin import BasePlugin


class MultiqcPlugin(BasePlugin):
    """
    MultiQC plugin.

    :Example:
    @multiqc(analysisDir='', )
    """
    plugin_name = 'multiqc'
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    is_server = False

    def __init__(self, *args, **kwargs):
        super(MultiqcPlugin, self).__init__(*args, **kwargs)

    def external_css(self):
        test_css = os.path.join(os.path.dirname(__file__), 'multiqc.css')
        return [{'multiqc_css': test_css}]

    def check_plugin_args(self, **kwargs):
        analysis_dir = kwargs.get('analysisDir')
        kwargs_str = ', '.join('%s=%r' % x for x in kwargs.items())
        self.logger.info('Running @%s(%s)' % (self.plugin_name, kwargs_str))
        if not analysis_dir:
            raise Exception('%s must have a analysisDir argument' % self.plugin_name)

    def render(self, **kwargs):
        analysis_dir = self.get_real_path('analysisDir')
        multiqc_path = self.multiqc(analysis_dir)
        if os.path.isfile(str(multiqc_path)):
            self.set_index('multiqc', multiqc_path, ftype='html')
            div_component = '<a href="%s" target="_blank">See Multiqc Report for More details.</a>'\
                            % self.get_net_path('multiqc')
            return [div_component, ]
