# -*- coding: utf-8 -*-
#
from __future__ import print_function
__author__ = 'xen'

class ModelBase(type):
    """
    Base model metaclass
    """
    def __new__(cls, name, bases, attrs):
        print("Create new class:", cls)
        print("Class bases:", bases)
        print("Class name:", name)
        print("Class attrs", attrs)
        return super(MyType, cls).__new__(cls, name, bases, newattrs)


class Model(object):
    __metaclass__ = ModelBase
    def __init__(self, *args, **kwargs):
        pass

