# -*- coding: utf-8 -*-
#
from __future__ import print_function
__author__ = 'xen'
import yaml


class ModelRegistry(object):
    models = {}

    @classmethod
    def resolve(cls, name):
        if name not in cls.models:
            return

        return cls.models[name]

    @classmethod
    def register(cls, model, name):
        assert name not in cls.models, 'Double registration of %r' % name
        cls.models[name]=model

    @classmethod
    def list(cls):
        return cls.models.keys()



class MetaModel(type):
    """
    Base model metaclass
    """
    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        abstract = getattr(meta, 'abstract', False)
        registername = attrs.pop('name', name.lower())

        cfg = {}
        if attrs.has_key('__yaml__'):
            cfg = yaml.load(open(attrs['__yaml__']))

        cfg.update(attrs)

        newbornclass = super(MetaModel, cls).__new__(cls, name, bases, cfg)

        if not abstract:
            #print("Register widget:", registername)
            ModelRegistry.register(newbornclass, registername)

        return newbornclass

class Model(object):
    __metaclass__ = MetaModel

    class Meta:
        abstract = True

