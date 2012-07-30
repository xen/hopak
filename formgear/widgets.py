# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os

from jinja2 import Environment, FileSystemLoader
from registry import Registry
from utils import widgets_path


widgetspath = widgets_path()


class NotFoundWidgetException(Exception):
    pass


class WidgetRegistry(Registry):
    NotFound = NotFoundWidgetException


class MetaWidget(type):
    """
    Class for all widgets
    """
    def __new__(cls, name, bases, attrs):
        #print("Forming new widget class:", cls)
        #print("Class bases:", bases)
        #print("Class name:", name)
        #print("Class attrs", attrs)
        meta = attrs.pop('Meta', None)
        abstract = getattr(meta, 'abstract', False)
        registername = attrs.pop('name', name.lower())
        newbornclass = super(MetaWidget, cls).__new__(cls, name, bases, attrs)

        if not abstract:
            newbornclass.load_macros()
            #print("Register widget:", registername)
            WidgetRegistry.register(newbornclass, registername)

        return newbornclass


class Widget(object):
    """
    Виджеты регистрируются в общем реестре и потом могут обратно резолвится
    через специальный реестр.

    Виджеты имеют следующие аттрибуты:

    hidden
       виджет не отображается в форме

    name
      удобное имя для виджета, по умолчанию подставляется имя класса

    template
      шаблон который занимается отображением. Внимание в шаблоне должны быть
      доступный определенный набор макросов для вызова. Для начала наверное что-то
      типа:

        * edit - режим редактирования в стандартной форме
        * view - режим просмотрта
        * table_edit - редактирование в табличной форме (для массового редактирования)
        * table_view - просмотр поля в табличном режиме
        * search_edit - в поисковой форме

    XXX: пока не решен вопрос с AJAX виджетами для которых нужны серверные методы

    """
    __metaclass__ = MetaWidget

    hidden = False
    error_class = 'error'
    css = None
    value = ""
    _type = "text"

    class Meta:
        abstract = True

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def render(self, field, state, env=None, **kw):
        if self.hidden:
            return ''

        macro = getattr(self, '_macro_%s' % state, None)
        assert macro, 'Widget %s have no macro named %r' % (
                self.__class__.__name__, state
        )
        return macro(field=field, widget=self, **kw)

    def itype(self):
        return self._type

    @classmethod
    def load_macros(cls):
        env = Environment(loader=FileSystemLoader(widgetspath))
        tmplt = env.get_template(cls.template+".html")
        mod = tmplt.module
        for macro_name, macro in mod.__dict__.items():
            if macro_name[0] == '_':
                continue

            setattr(cls, '_macro_%s' % macro_name, macro)


# html5 input fields, support status here http://www.w3schools.com/html5/html5_form_input_types.asp
# color
# date
# datetime
# datetime-local
# email
# month
# number
# range
# search
# tel
# time
# url
# week

class DateWidget(Widget):
    """
    DateWidget
    """
    template = 'string'
    alter_names = ('date',)


class StringWidget(Widget):
    """
    InputWidget <input type="text"/>
    """
    _type = 'text'
    alter_names = ('string',)
    template = 'string' # We will try to find text.html template in widgets directory
    value = ""

class PhoneWidget(Widget):
    alter_names = ('tel', 'phone', )
    _type = 'tel'
    template = 'string'

class TextWidget(Widget):
    """
    TextWidget <textarea />
    """
    alter_names = ('text',)
    template = 'text'


class PasswordWidget(StringWidget):
    """
    PasswordWidget <input type="password" />
    """
    alter_names = ('password', 'passw')
    template = 'password'
    _type = 'password'

class BooleanWidget(Widget):
    """" Simple checkbox """
    alter_names = ('boolean', 'bool')
    template = 'boolean'

class EmailWidget(StringWidget):
    """ Email input filed
    """
    alter_names = ('email',)
    template = 'email'
    _type = 'email'

class CheckboxWidget(Widget):
    """
    CheckboxWidget <input type="checkbox" />
    """
    alter_names = ('checkbox',)
    template = 'checkbox'


class PricerangeWidget(Widget):
    alter_names = ('pricerange',)
    template = 'pricerange'


class TimerangeWidget(Widget):
    alter_names = ('timerange',)
    template = 'timerange'


class SelectWidget(Widget):
    """ One choice with multiple list
    """
    alter_names = ('select',)
    template = 'select'

'''class ImageWidget(Widget):
    """
    http://blueimp.github.com/jQuery-File-Upload/
    """
    pass'''

class MarkdownWidget(Widget):
    alter_names = ('markdown',)
    template = 'markdown'
