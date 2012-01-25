# -*- coding: utf-8 -*-
#
from __future__ import print_function
from functools import partial
from formgear.fields import FieldsRegistry
from formgear.widgets import WidgetRegistry
from registry import Registry

__author__ = 'xen'
import yaml

class NotFoundModelException(Exception):
    pass

class ModelRegistry(Registry):
    NotFound = NotFoundModelException

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

        fields = []
        for field in cfg.pop('fields', []):
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
            fields.append((field.pop('name'), f(widget = wdgt, **field)))

        forms = {}
        for form in cfg.pop('forms', []):
            forms[form['name']] = form['fields']

        cfg.update(attrs)
        newbornclass = super(MetaModel, cls).__new__(cls, name, bases, cfg)

        for fname, ffunc in fields:
            setattr(newbornclass, fname, ffunc)

        newbornclass._fields = [
            ffunc for _fname, ffunc in fields
        ]

        newbornclass.forms = forms

        if not abstract:
            #print("Register widget:", registername)
            ModelRegistry.register(newbornclass, registername)

        return newbornclass

class Model(object):
    __metaclass__ = MetaModel

    class Meta:
        abstract = True

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, name):
        """Attrubute-style field and forms access.
        """
        try:
            if name in self._fields:
                return getattr(self, name)
        except AttributeError:
            pass
        if name in self.forms:
            return self.form(fields=self.forms[name])
        raise KeyError(name)

    def __setitem__(self, name, value):
        raise NotImplementedError

    def form(self, fields=[]):
        """ Renders form from model instance
        """
        if fields:
            raise NotImplementedError
        else:
            return self._fields
