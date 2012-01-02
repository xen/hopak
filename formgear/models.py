# -*- coding: utf-8 -*-
#
from __future__ import print_function
from functools import partial
from formgear.fields import FieldsRegistry
from formgear.widgets import WidgetRegistry

__author__ = 'xen'
import yaml

class NotFoundModelException(Exception):
    pass

class ModelRegistry(object):
    models = {}

    @classmethod
    def resolve(cls, name):
        if ModelRegistryModelRegistry.widgets.has_key(name.lower()):
            return ModelRegistry.models[name.lower()]
        else:
            raise NotFoundModelException(name)

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


        new_fields = []
        if cfg.has_key('fields'):

            for field in cfg['fields']:
                # extracts widget information
                widget = field.pop('widget', 'text')
                if type(widget) == type({}):
                    wdgt = partial(WidgetRegistry.resolve(widget.pop('type', 'text')), **widget)
                else:
                    wdgt = WidgetRegistry.resolve(widget)
                # actual work with fields
                if field.has_key('name'):
                    f = FieldsRegistry.resolve(field.pop('type', 'string').lower())
                else:
                    raise ParsingException
                # XXX: here is missed part with validators
                new_fields.append((field.pop('name'), f(widget = wdgt, **field)))
            del cfg['fields']


        cfg.update(attrs)
        newbornclass = super(MetaModel, cls).__new__(cls, name, bases, cfg)

        for fname, ffunc in new_fields:
            setattr(newbornclass, fname, ffunc)

        if not abstract:
            #print("Register widget:", registername)
            ModelRegistry.register(newbornclass, registername)

        return newbornclass

class Model(object):
    __metaclass__ = MetaModel

    class Meta:
        abstract = True

