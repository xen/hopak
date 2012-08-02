# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os
import yaml
import mongo

from formgear.fields import FieldsRegistry
from formgear.widgets import WidgetRegistry
from registry import Registry
from formgear.exceptions import *
from formgear.utils import yamls_files, file_resolve

from jinja2 import Environment, PackageLoader

__author__ = 'xen'

yamlsfiles = yamls_files()


class ModelRegistry(Registry):
    NotFound = NotFoundModelException

def model_wrap(model, **wrap_kw):
    def __init__(self, *a, **kw):
        kw.update(wrap_kw)
        model.__init__(self, *a, **kw)

    attrs = {"__init__": __init__, "__fake__": True}
    return MetaModel(model.__name__, (model,), attrs)

class FormWrap(object):
    def __init__(self, forms, model):
        self.model = model

        self.forms = forms

    def get(self, name, silent=None):
        """ Return form fields as dict for a class:

            >>> model.form(name='default')
            [('email', <formgear.fields.StringField object at 4529231184>), ...)]
            >>> model.form(name='search')
            KeyError: "Form 'search' not found for model <class 'admin.auth.models.User'>"

        There is always 'default' form which contaions all model field.

        If `silent` param provided then wrong form name don't caught exception

        """
        name = name or 'default'
        for form in self.forms:
            if form['name'] == name:
                #print(name, ': ', form)
                return form
        if silent:
            return None
        else:
            raise KeyError("Form %r not found for model %r" % (name, self.model))

    def field(self, name):
        return self.model._fields_dict[name]

    def __call__(self, name=None, fields=[], **kw):
        if not fields:
            form = self.get(name or self.model.subform, **kw)
            if form:
                fields = form['fields']

        ret = [
                (name, self.field(name))
                for name in fields
        ]
        return ret


    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if self.get(name) is None:
                raise

        if isinstance(self.model, type):
            model = model_wrap(self.model, subform=name)
            model.subform = name
            return model

        obj = self.model.__class__(subform=name)
        obj._fields = self.model._fields
        return obj


class MetaModel(type):
    """
    Base model metaclass
    """
    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        abstract = getattr(meta, 'abstract', False)
        fake = attrs.pop('__fake__', None)
        registername = attrs.pop('name', name.lower())

        cfg = {}
        # we have search __yaml__ attribute only, when we
        # have initialize a subclass of formgear.models.Model
        if not abstract:

            # try to find out by __yaml__ or by class name
            # __yaml__ = "order" or class Order(Models):
            ypath = attrs.get('__yaml__') or name.lower()

            ypath = yamlsfiles.get(ypath, ypath)
            if not os.access(ypath, 0):
                raise YamlEntryNotFoundInListException

            cfg = yaml.safe_load(open(ypath))

            attrs["__yaml__"] = ypath

        # this block should make model registry list looks better
        _descr = ''
        if cfg.get('description', None):
            _descr = cfg.get('description')
        if attrs.get('__doc__', None) and len(attrs.get('__doc__')):
            _descr = attrs.get('__doc__')
        else:
            attrs['__doc__'] = _descr
        _title = registername
        if cfg.get('title', None):
            _title = cfg.get('title')

        cfg['_name'] = registername
        cfg['_descr'] = _descr
        cfg['_title'] = _title

        fields = []
        key_fields = attrs.get('__key__', [])
        if not isinstance(key_fields, (list,tuple)):
            key_fields = []

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

            file_resolve(field, "choices", ypath)

            if field['name'] in key_fields:
                field['required'] = True

            new_field = field_class(widget = wdgt, **field)

            # actual work with fields
            # XXX: here is missed part with validators
            fields.append((field.pop('name'), new_field))

        forms = []
        forms.extend(cfg.pop('forms', []))
        forms.append({
            "name": "default",
            "fields": [
                fname
                for fname, _field in fields
                if hasattr(_field, 'title')
            ],
        })

        cfg.update(attrs)
        newbornclass = super(MetaModel, cls).__new__(cls, name, bases, cfg)

        for fname, ffunc in fields:
            setattr(newbornclass, fname, ffunc)

        newbornclass._fields = fields
        newbornclass._fields_dict = dict(fields)


        newbornclass.form = FormWrap(forms, newbornclass)

        if not abstract and not fake:
            ModelRegistry.register(newbornclass, registername)

        return newbornclass

class Model(object):
    __metaclass__ = MetaModel
    subform = None

    class Meta:
        abstract = True

    def __init__(self, data=None, subform=None, _id=None, _raw=False, **kw):
        assert data is None or not kw, 'Pass data in one way'
        if data:
            kw = data
        if _id:
            self._id = _id

        self.subform = subform
        form = self.form.get(subform)
        self.render_form = self._render_form

        subform_fields = []
        all_fields = []
        for name, _field in self._fields:
            field = _field.reinstance()
            all_fields.append((name,field))

            if name in form['fields']:
                subform_fields.append((name, field))

        self._fields = subform_fields
        self._fields_dict = dict(subform_fields)
        self._all_fields_dict = dict(all_fields)
        self.form = FormWrap(self.form.forms, self)

        self.update(kw, raw=_raw)
        if _id:
            self.lock_id()

    def update(self, data=None, raw=False, **kw):
        assert data is None or not kw, 'Pass data in one way'
        kw = data or kw
        if callable(getattr(kw, 'items', None)):
            kw = kw.items()

        for name, val in kw:

            field = self._field(name, raw=raw)
            if not field:
                continue

            if getattr(field, 'locked', False):
                continue

            field.value = val

    def items(self):
        for name, field in self._fields:
            yield name, field.value

    def __iter__(self):
        return iter(self.form(self.subform))

    def _field(self, name, raw=False):
        if raw:
            return self._all_fields_dict.get(name)
        return self._fields_dict.get(name)

    # getattr gives access to all loaded fields
    def __getattribute__(self, name):
        try:
            fields = object.__getattribute__(self,'_all_fields_dict')
            if name in fields:
                return fields.get(name).value

        except AttributeError:
            pass

        return object.__getattribute__(self, name)

    # setattr gives acces only to fields available in this subform
    def __setattr__(self, name, value):
        try:
            fields = object.__getattribute__(self,'_fields_dict')
            if name in fields:
                fields[name].value = value
                return
            elif name in object.__getattribute__(self,'_all_fields_dict'):
                raise TypeError(
                    "Refused to update field %s missing in subform %s" %
                    (name, self.subform)
                )

        except AttributeError:
            pass

        return object.__setattr__(self, name, value)

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
            for name,field in self._all_fields_dict.items()
        ])

        if '_id' in doc:
            pass
        elif hasattr(self, 'key'):
            _id = self.key()
            if not (_id is None):
                doc['_id'] = _id
        elif hasattr(self, '_id'):
           doc['_id'] = self._id

        return doc

    def lock_id(self):
        if not hasattr(self.__class__, '__key__'):
            return

        if not isinstance(self.__key__, (list, tuple)):
            return

        for name in self.__key__:
            field = self._field(name)
            if not field:
                continue

            field.locked = True

    @classmethod
    def __key_type(cls, value):
        import bson
        if not hasattr(cls, '__key__'):
            return bson.objectid.ObjectId(value)

        return value

    def key(self):
        if not hasattr(self.__class__, '__key__'):
            return getattr(self, '_id', None)

        if isinstance(self.__key__, (list, tuple)):
            if self.__key__[0] == '_id':

                # don`t generate random id twice
                if hasattr(self, '_id'):
                    return self._id

                import bson
                names = self.__key__[1:]
                vals = [
                        unicode(bson.objectid.ObjectId())
                ]
            else:
                names = self.__key__
                vals = []

            vals.extend([
                getattr(self, fieldname)
                for fieldname in names
            ])
            assert None not in vals, "Field must have a value \
if specified in __key__"

            return unicode.join(u"::", vals)

        elif isinstance(self.__key__, basestring):
            return getattr(self, self.__key__)
        elif callable(self.__key__):
            return self.__key__()
        elif hasattr(self.__class__.__key__, 'getter'):
            return self.__key__

        assert False, "Who is Mr. __key__?"

    def save(self):
        _id = getattr(self, '_id', None)
        self._id = mongo.save(self.kind(), self.to_mongo(), _id)
        return self._id

    @classmethod
    def all(cls, **kw):
        return [
                cls(_raw=True, **data)
                for data in
                mongo.find(cls.kind(), **kw)
        ]

    @classmethod
    def kind(cls):
        return cls.__name__.lower()

    @classmethod
    def count(cls):
        return cls.all().count()

    @classmethod
    def get(cls, key=None, **kw):
        if not kw and key:
            kw = {"_id": cls.__key_type(key)}

        data = list(cls.all(**kw)[:1])
        if not data:
            return

        return data[0]

    @classmethod
    def delete(cls, _filter):
        if not isinstance(filter, dict):
            _filter = {"_id": cls.__key_type(_filter)}

        mongo.remove(cls.kind(), _filter)

    def render_form(self, env=None, state='edit', form=None, **kw):
        """
        Form rendering entry point.
        This method can be used to render both forms (model subclasses)
        and form instances (aka objects).
        Returns plain HTML.


        :param env: jinja2 envirement object used for template rendering.
        This param *should* be ommited when calling from jinja2 templates.
        Passed environment should have "form.html" template and widget
        templates availible.

        :param state: controls which state of form should be displayed.
        Common states are "edit" and "table_edit"
        Form states and field states are different concepts.
        Form states are implemented as macros in "form.html" template

        :param form: subform name used when rendering this form/model.
        Subform is a named set (slice) of fields, specified in model.yaml.
        This param should not be passed to forms or objects with subform
        attribute set to value other than None
        When no subforms defined in yaml, no param passed and no "subform"
        attribute set, all fields are rendered

        Default field set can be overriden by specifying "default" subform in
        yaml.
        """
        #print(form, '-', self.subform)
        assert form is None or self.subform is None
        env = env or Environment(loader=PackageLoader('formgear'))
        template = env.get_template('form.html')
        m = getattr(template.module, state, None)

        fields = self.form(form or self.subform or 'default')

        return m(form = fields, **kw)

    _render_form = render_form
    render_form.environmentfunction = True
    render_form = classmethod(render_form)
