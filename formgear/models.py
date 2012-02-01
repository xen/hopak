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
                continue

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
        for name, field in self._fields:
            if not hasattr(field, 'validate'):
                continue

            valid = field.validate()
            if not valid:
                return

        return True

    def to_mongo(self):

        doc = dict([
            (name, field.to_mongo)
            for name,field in self._fields
        ])

        if '_id' in doc:
            pass
        elif hasattr(self, '_id'):
            doc['_id'] = self._id
        elif hasattr(self, 'key'):
            _id = self.key()
            if not (_id is None):
                doc['_id'] = _id

        return doc

    def key(self):
        if not hasattr(self.__class__, '__key__'):
            return

        if isinstance(self.__key__, (list, tuple)):
            if self.__key__[0] == '_id':
                import pymongo
                names = self.__key__[1:]
                vals = [
                        unicode(pymongo.objectid.ObjectId())
                ]
            else:
                names = self.__key__
                vals = []

            vals.extend([
                getattr(self, fieldname).value
                for fieldname in names
            ])
            assert None not in vals, "Field must have value \
                    if specified in __key__"

            return unicode.join(u"::", vals)

        elif isinstance(self.__key__, basestring):
            return getattr(self, self.__key__).value
        elif callable(self.__key__):
            return self.__key__()
        elif hasattr(self.__class__.__key__, 'getter'):
            return self.__key__

        assert False, "Who is Mr. __key__?"

    def save(self):
        import mongo
        mongo.save(self.kind(), self.to_mongo())

    @classmethod
    def all(cls):
        import mongo
        return mongo.find(cls.kind())

    @classmethod
    def kind(cls):
        return getattr(cls, '__yaml__', None) or cls.__name__

    @classmethod
    def count(cls):
        return cls.all().count()
