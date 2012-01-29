# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os
import yaml

from formgear.fields import FieldsRegistry
from formgear.widgets import WidgetRegistry
from registry import Registry
from formgear.exceptions import *
from formgear.utils import yamls_files

__author__ = 'xen'

yamlsfiles = yamls_files()


class ModelRegistry(Registry):
    NotFound = NotFoundModelException


class MetaModel(type):
    """
    Base model metaclass
    """
    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        abstract = getattr(meta, 'abstract', False)
        registername = attrs.pop('name', name.lower())

        cfg = {}
        # we have search __yaml__ attribute only, when we 
        # have initialize a subclass of formgear.models.Model
        if not abstract:

            if not attrs.has_key('__yaml__'):
                raise YamlAttributeNotFoundException

            ypath = attrs['__yaml__']

            ypath = yamlsfiles.get(ypath, ypath)
            if not os.access(ypath, 0):
                raise YamlEntryNotFoundInListException

            cfg = yaml.safe_load(open(ypath))


        fields = []
        for field in cfg.pop('fields', []):
            if 'name' not in field:
                raise ParsingException("Oops, we found nameless field!")

            field_typ = field.pop('type', 'string')
            field_class = FieldsRegistry.resolve(field_typ)

            # extracts widget information
            widget = field.pop('widget', field_class.widget)

            if isinstance(widget, dict):
                widget_typ = widget.pop('type', field_class.widget)
                widget_kw = widget
            else:
                widget_typ = widget
                widget_kw = {}

            if isinstance(widget_typ, basestring):
                widgt_class = WidgetRegistry.resolve(widget_typ)
            else:
                widgt_class = widget_typ

            wdgt = widgt_class(**widget_kw)
            # actual work with fields

            # XXX: here is missed part with validators
            fields.append((field.pop('name'), field_class(widget = wdgt, **field)))

        forms = {}
        forms['default'] = [
                fname
                for fname, _field in fields
                if hasattr(_field, 'title')
        ]
        for form in cfg.pop('forms', []):
            forms[form['name']] = form['fields']

        cfg.update(attrs)
        newbornclass = super(MetaModel, cls).__new__(cls, name, bases, cfg)

        for fname, ffunc in fields:
            setattr(newbornclass, fname, ffunc)

        newbornclass._fields = fields

        newbornclass.forms = forms

        if not abstract:
            #print("Register widget:", registername)
            ModelRegistry.register(newbornclass, registername)

        return newbornclass

class Model(object):
    __metaclass__ = MetaModel

    class Meta:
        abstract = True

    def __init__(self, data=None, **kw):
        fields = dict(self._fields)
        assert data is None or not kw, 'Pass data in one way'
        if data:
            kw = data
        for name, val in kw.items():
            if name not in fields:
                raise TypeError("%r has no field %r" % (self, name))

            field = getattr(self, name)
            field.value = val

    def items(self):
        for name, field in self._fields:
            yield name, field.value

    def __iter__(self):
        for name, field in self._fields:
            yield name, field

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

    def form(self, name='default', fields=[]):
        """ Renders form from model instance
        """
        if not fields and name in self.forms:
            fields = self.forms[name]

        fdict = dict(self._fields)

        return [
                (name, fdict[name])
                for name in fields
        ]

    def validate(self):
        return True

    def to_mongo(self):
        return dict(self.items())

    def save(self):
        import mongo
        mongo.save(self.__class__.__name__, self.to_mongo())
