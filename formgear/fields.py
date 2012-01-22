# -*- coding: utf-8 -*-
import itertools
#from mongoengine.base import BaseField as MongoField

import controllers
from registry import Registry

class NotFoundFieldException(Exception):
    pass

class FieldsRegistry(Registry):
    """ Registry needed to resolve fields from YAML file """
    fields = {}
    NotFound = NotFoundFieldException

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

class BaseField(object):
    """ BaseField is very similar to MongoEngine fields.
    """

    __metaclass__ = MetaField
    # Fields may have _types inserted into indexes by default
    _index_with_types = True
    _geo_index = False

    def __init__(self, db_field=None, required=False, default=None,
                 unique=False, unique_with=None, primary_key=False,
                 validators=None, **kw):
        """
        Params:

          * db_field - set explicit field name in database
          * required - quick alias for validator.Required
          * title - field name
          * default=None - default value
          * unique=False - mongodb unique field index
          * unique_with=None - mongodb unique_with field index
          * primary_key=False - mongodb field index for primary_key
          * validators=None - set of validators from controllers collection (or your own)
          * description=None - field help text description
          * widget - widget to represent field value

        """
        self.db_field = db_field if not primary_key else '_id'

        self.required = required or primary_key
        self.unique = bool(unique or unique_with)
        self.unique_with = unique_with
        self.default = default


        if validators:
            if controllers.Required in validators:
                self.required = True
        if required:
            self.required = True
            if controllers.Required not in validation:
                validation.append(validators.Required)

        self.__dict__.update(kw)

    def validate(self, value):
        """Perform validation on a value.
        """
        pass

    def translate(self, msgid):
        """ Use the translator passed to the renderer of this field to
        translate the msgid into a term.  If the renderer does not have a
        translator, this method will return the msgid."""
        translate = getattr(self.renderer, 'translate', None)
        if translate is not None:
            return translate(msgid)
        return msgid

    def __repr__(self):
        return '<%s.%s object at %d>' % (
            self.__module__,
            self.__class__.__name__,
            id(self)
            )

    def __call__(self, state="view", **kwargs):
        return self.widget.render(self, state, **kwargs)

class TextField(BaseField):

    alter_names = ('text',)

    def __init__(self, **kwargs):
        self.default = ''
        self.widget_class = kwargs.get('widget')
        self.widget = self.widget_class()

class StringField(BaseField):

    alter_names = ('string',)

    def __init__(self, **kwargs):
        self.widget_class = kwargs.get('widget')
        self.widget = self.widget_class()
