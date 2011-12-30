# -*- coding: utf-8 -*-
#
from __future__ import print_function
__author__ = 'xen'
import yaml


from widgets import *

class ModelRegistry(object):
    models = []


class ModelBase(type):
    """
    Base model metaclass
    """
    def __new__(cls, name, bases, attrs):
        print("Create new class:", cls)
        print("Class bases:", bases)
        print("Class name:", name)
        print("Class attrs", attrs)

        # register models in global list
        ModelRegistry.models.append(cls)

        newattrs = {}
        cfg = {}
        if attrs.has_key('__yaml__'):
            cfg = yaml.load(open(attrs['__yaml__']))

        cfg.update(attrs)

        return super(ModelBase, cls).__new__(cls, name, bases, cfg)

class Model(object):
    __metaclass__ = ModelBase

