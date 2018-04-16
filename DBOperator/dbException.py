# -*- coding: UTF-8 -*-
"""
包含一些自定义异常
"""


class ClassErrorException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{0} is not iterator".format(self.value)
