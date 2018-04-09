# -*- coding: utf-8 -*-
"""
此文件包含了一些自定义异常类，方便提示错误
"""


class AnalysisError(Exception):
    def __init__(self,value):
        """
        当解析配置文件出错时，抛出此异常

        :param value: 解析异常的 key-name
        """
        self.value = value

    def __str__(self):
        return "Analyse config error, key: {0}".format(self.value)


class LackDataError(Exception):
    def __init__(self,value):
        """
        当缺少某个数据时，抛出此异常

        :param value: 所缺少的数据的 name
        """
        self.value = value

    def __str__(self):
        return "Lack {0} data".format(self.value)