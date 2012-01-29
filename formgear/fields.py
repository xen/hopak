# -*- coding: utf-8 -*-
import itertools
#from mongoengine.base import BaseField as MongoField

import datetime, re


import controllers
import widgets
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
    widget = widgets.StringWidget

    def __init__(self, db_field=None, required=False, default=None,
                 unique=False, unique_with=None, primary_key=False,
                 validators=[], widget=None, **kw):
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

        self.validators = validators
        if controllers.Required in self.validators:
            self.required = True
        if required:
            self.required = True
            if controllers.Required not in self.validators:
                self.validators.append(controllers.Required)

        if widget:
            self.widget = widget

        self.__dict__.update(kw)
        self.value = None

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

class StringField(BaseField):
    """ Simple string
    """

    alter_names = ('string',)

    def __init__(self, regex=None, max_length=None, min_length=None, **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length
        super(StringField, self).__init__(**kwargs)

class TextField(BaseField):
    """ Plain text field.
    XXX: Add text processors, may be including typography.
    """
    alter_names = ('text',)
    widget = widgets.TextWidget

    def __init__(self, max_length=None, min_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super(TextField, self).__init__(**kwargs)


class DateField(BaseField):
    alter_names = ('date', )

    format='%Y/%m/%d'
    # self.data = datetime.datetime.strptime(date_str, self.format).date()
    def __init__(self, **kwargs):
        """
        """
        pass

class DateTimeField(BaseField):

    alter_names = ('datetime',)

class TimeField(BaseField):
    alter_names = ('time', )

class IntegerField(BaseField):
    alter_names = ('int', 'integer', )

class BooleanField(BaseField):
    alter_names = ('bool', 'boolean', )

class EmailField(BaseField):
    alter_names = ('email', )

class FloatField(BaseField):
    alter_names = ('float', )

class URLField(BaseField):
    alter_names = ('url', 'link', )

    #XXX: Y NO ccTLD like xn--shitshitshit domains?
    URL_REGEX = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

    def __init__(self, verify_exists=False):
        self.verify_exists = verify_exists
        super(URLField, self).__init__(**kwargs)


class FileField(BaseField):
    alter_names = ('file', 'blob', )

class ImageField(BaseField):
    alter_names = ('img', 'image', )

class GeoPointField(BaseField):
    alter_names = ('geo', 'geopoint', )
