# -*- coding: utf-8 -*-

class PluginValueError(ValueError):
    pass


class PluginBase(object):
    keyword = ''
    description = ''

    def __init__(self):
        if not self.keyword:
            raise PluginValueError('请设置插件关键字')

    def process(self, data):
        raise NotImplementedError
