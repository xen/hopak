# -*- coding: utf-8 -*-
#
from __future__ import print_function
from formgear.fields import FieldsRegistry
from formgear.widgets import WidgetRegistry

__author__ = 'xen'
import yaml


class ModelRegistry(object):
    models = {}

    @classmethod
    def resolve(cls, name):
        return ModelRegistry.models[name]

    @classmethod
    def register(cls, model, name):
        ModelRegistry.models[name]=model

    @classmethod
    def list(cls):
        return ModelRegistry.models.keys()

class ParsingException(Exception):
    pass

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
            cfg = yaml.safe_load(open(attrs['__yaml__']))

        if cfg.has_key('fields'):
            new_fields = ()
            for field in cfg['fields']:
                # extracts widget information
                widget = field.pop('widget', 'text').lower()
                if type(widget) == type({}):
                    wdgt = WidgetRegistry.resolve(widget.pop('type', 'text'))(**widget)
                else:
                    wdgt = WidgetRegistry.resolve(widget)()

                typ = field.pop('type', 'string').lower()
                if field.has_key('name'):
                    f = FieldsRegistry.resolve(typ)
                else:
                    raise ParsingException
                new_fields.append()


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

