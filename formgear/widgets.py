# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os

from jinja2 import Environment, FileSystemLoader
from registry import Registry
from utils import widgets_path


widgets_path = widgets_path()

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

    class Meta:
        abstract = True

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def render(self, field, state, env=None, **kw):
        """ Here is should be field rendering
        """
        if not env:
            env = Environment(loader=FileSystemLoader(widgets_path))
        tmplt = env.get_template(self.template+".html")
        macro = getattr(tmplt.module, state, None)
        if not macro:
            return '' # XXX: output red text?

        return macro(field=field, **kw)


class StringWidget(Widget):
    """
    InputWidget <input type="text"/>
    """
    alter_names = ('string',)
    template = 'string' # We will try to find text.html template in widgets directory


class TextWidget(Widget):
    """
    TextWidget <textarea />
    """
    alter_names = ('text',)
    templates = 'text'
