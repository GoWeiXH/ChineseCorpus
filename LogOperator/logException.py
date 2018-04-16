# -*- coding: UTF-8 -*-
class LevelException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{0} cannot be selected as a level".format(self.value)