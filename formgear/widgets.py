# -*- coding: utf-8 -*-
#
from __future__ import print_function
import os

from jinja2 import Environment, FileSystemLoader
from registry import Registry

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

    ? hidden
       виджет не отображается в форме

    error_class
       CSS класс для отображения ошибки
       По умолчанию "error"

    css_class
       CSS класс для обображения контейнера виджета

    resourcess
       дополнительные media файлы которые требуется подключить для отображения
       этого виджета в админке, словарь

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

    # hidden = False
    error_class = 'error'
    css_class = None
    requirements = ()

    class Meta:
        abstract = True

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def serialize(self, field, value, state='edit'):
        """
        Параметры:

        field
          объект поля контент класса

        value
          значение поля, передается в шаблон

        state
          какой макрос шаблона будет вызван для отображения в HTML
        """
        raise NotImplementedError

    def deserialize(self, field, pstruct):
        """
        """
        raise NotImplementedError

    def render(self, field, state, env=None, **kw):
        """ Here is should be field rendering
        """
        if not env:
            path = os.path.join(os.path.dirname(__file__), 'templates')
            env = Environment(loader=FileSystemLoader(path))
        tmplt = env.get_template(self.template)
        macro = getattr(tmplt.module, state, None)
        if not macro:
            return '' # XXX: output red text?

        return macro(field=field, **kw)

class StringWidget(Widget):
    """
    Текстовый виджет. Служит для создания поля в формате <input type="{{type}}" />.

    Получает аргументы:

    size
      Атрибут HTML поля size

    tagtype
      для поддержки HTML5 полей, по умолчанию text

    strip
      для обрезания пробелов до и после текста, по умолчанию True

    placeholder
      HTML5 атрибут placeholder, по умолчанию пусто

    """
    name = 'stringwidget'
    template = 'widgets/string.html'
    size = None
    strip = True
    placeholder = ''
    tagtype = 'text'
    alter_names = ('string', 'str', )

    def serialize(self, field, cstruct, state):
        if not cstruct:
            cstruct = ''
        return field.renderer(self.template, field=field, cstruct=cstruct, state=state)

    def deserialize(self, field, pstruct):
        if not pstruct:
            return None
        if self.strip:
            pstruct = pstruct.strip()
        if not pstruct:
            return None
        return pstruct

class TextWidget(Widget):
    alter_names = ('text', 'textarea', )
    template = 'widgets/text.html'

class WYSIWYGWidget(Widget):
    name = 'wysiwyg'
    template = 'widgets/wysiwyg.html'
    size = None
    strip = False
    placeholder = ''

    def serialize(self, field, cstruct, state):
        raise NotImplemented

    def deserialize(self, field, pstruct):
        raise NotImplemented

