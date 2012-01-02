# -*- coding: utf-8 -*-
#
import itertools
from mongoengine.base import BaseField as MongoField

class NotFoundFieldException(Exception):
    pass

class FieldsRegistry(object):
    fields = {}

    @classmethod
    def resolve(cls, name):
        if FieldsRegistry.fields.has_key(name.lower()):
            return FieldsRegistry.fields[name.lower()]
        else:
            raise NotFoundFieldException(name)

    @classmethod
    def register(cls, field, name):
        # XXX: Resolve when this Field is already registered
        if getattr(field, 'alter_names', None):
            for x in field.alter_names:
                FieldsRegistry.fields[x]=field
        FieldsRegistry.fields[name]=field

    @classmethod
    def list(cls):
        return FieldsRegistry.fields.keys()

class MetaField(type):
    """
    Class for all widgets
    """
    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        abstract = getattr(meta, 'abstract', False)
        registername = attrs.pop('name', name.lower())
        newbornclass = super(MetaField, cls).__new__(cls, name, bases, attrs)

        if not abstract:
            #print("Register widget:", registername)
            FieldsRegistry.register(newbornclass, registername)

        return newbornclass

class BaseField(MongoField):
    __metaclass__ = MetaField

    def __init__(self, **kwargs):
        base_params = ('db_field', 'name', 'required', 'default',
                         'unique', 'unique_with', 'primary_key',
                         'validation', 'choices', 'verbose_name', 'help_text')
        kw = {}
        for x in base_params:
            if kwargs.has_key(x): kw[x]= kwargs[x]
        super(BaseField, __init__, **kw)

    def __repr__(self):
        return '<%s.%s object at %d>' % (
            self.__module__,
            self.__class__.__name__,
            id(self),
            )

class TextField(BaseField):

    alter_names = ('text',)

    def __init__(self, **kwargs):
        self.default = ''

class StringField(BaseField):

    alter_names = ('string',)

    def __init__(self, **kwargs):
        pass