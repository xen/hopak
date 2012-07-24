# -*- coding: utf-8 -*-

import datetime, re

import controllers
import widgets
from registry import Registry
from formgear.exceptions import InvalidValue

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


def init_partial(real):
    def init_partial(self, *a, **kw):
        self._partial = a, kw
        return real(self, *a, **kw)

    return init_partial


class BaseField(object):
    """ BaseField is very similar to MongoEngine fields.
    """

    __metaclass__ = MetaField
    # Fields may have _types inserted into indexes by default
    _index_with_types = True
    _geo_index = False
    widget = widgets.StringWidget

    @init_partial
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

        self.validators = controllers.lookup(validators)
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

    def validate(self):
        """Perform validation on a value.
        """
        ret = True
        self.errors = []
        for validator in self.validators:
            if isinstance(validator, type):
                validator = validator()

            try:
                validator(self, self.value)
            except InvalidValue, e:
                ret = False
                self.errors.append(e.args[1])
        return ret

    def reinstance(self):
        a, kw = self._partial
        return self.__class__(*a, **kw)

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

    def __unicode__(self):
        return unicode(self.value)

    __str__ = __unicode__

    def __call__(self, state="edit", **kwargs):
        return self.widget.render(self, state, **kwargs)

    def clear(self):
        self._value = None

    def set_value(self, val):
        self._value = val

    def get_value(self):
        val = self._value or self.default

        if val:
            short, _val = self.shortcut(val)
            if short:
                val = _val

        return val

    value = property(get_value, set_value)

    def shortcut(self, value):
        return False, None

    @property
    def to_mongo(self):
        if hasattr(self, '__mongo__'):
            val = self.__mongo__(self.value)
        else:
            val = self.value

        return val


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
    type = 'date'

    def shortcut(self, value):
        if value == 'now':
            return True, datetime.datetime.now()
        elif value == 'today':
            return True, datetime.datetime.today()

        return False, None

    def validate(self):
        if isinstance(self.value, datetime.datetime):
            return True

        from dateutil import parser
        try:
            self.value = parser.parse(self.value or '')
        except ValueError:
            return

        return True


class TimeField(BaseField):
    alter_names = ('time', )


class IntegerField(BaseField):
    alter_names = ('int', 'integer', )


class BooleanField(BaseField):
    alter_names = ('bool', 'boolean', )

    def shortcut(self, value):
        return True, bool(value)

class EmailField(BaseField):
    alter_names = ('email', )

    def validate(self):
        ret = '@' in self.value
        if not ret:
            self.errors = [
                    u"Wrong email format",
            ]
        return ret


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


class TimerangeField(BaseField):
    alter_name = ('timerange')
    widget = widgets.TimerangeWidget


class CheckboxField(BaseField):
    alter_names = ('checkbox',)
    choices = {}
    widget = widgets.CheckboxWidget

    def clear(self,):
        self._value = []

    def set_value(self, val):

        oldval = getattr(self, '_value', None)
        if not isinstance(oldval, list):
            self._value = [] if oldval is None else [oldval]

        if isinstance(val, (list, tuple)):
            self._value = val
        else:
            self._value.append(val)

    value = property(BaseField.get_value, set_value)


class StructField(BaseField):
    alter_names = ('struct',)


class PathField(StringField):
    alter_names = ('pathfield',)

    def set_value(self, val):
        if val:
            if not val.startswith("/"):
                val = "/%s" % (val,)
            self._value = val

    value = property(BaseField.get_value, set_value)
