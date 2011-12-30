# -*- coding: utf-8 -*-
#

__author__ = 'xen'

from formgear.models import Model, ModelRegistry

class User(Model):
    __yaml__ = 'test/data/doctype.yaml'

print ModelRegistry.list()