# -*- coding: utf-8 -*-
#
import itertools
from mongoengine.base import BaseField as MongoField

class FieldsRegistry(object):
    fields = {}

    @classmethod
    def resolve(cls, name):
        return FieldsRegistry.fields[name]

    @classmethod
    def register(cls, field, name):
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

    def __repr__(self):
        return '<%s.%s object at %d>' % (
            self.__module__,
            self.__class__.__name__,
            id(self),
            )

class TextField(BaseField):

    def __init__(self, default='', help_text='', primary_key=False, unique=False):
        self.default = ''