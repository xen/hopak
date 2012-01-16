# -*- coding: utf-8 -*-
#
from __future__ import print_function

from jinja2 import Environment, FileSystemLoader

class NotFoundWidgetException(Exception):
    pass

class WidgetRegistry(object):
    widgets = {}

    @classmethod
    def resolve(cls, name):
        if WidgetRegistry.widgets.has_key(name.lower()):
            return WidgetRegistry.widgets[name.lower()]
        else:
            raise NotFoundWidgetException(name)

    @classmethod
    def register(cls, widget, name):
        # XXX: I'm not sure about that. Don't looks healthy
        if getattr(widget, 'alter_names', None):
            for x in widget.alter_names:
                WidgetRegistry.widgets[x]=widget
        WidgetRegistry.widgets[name]=widget

    @classmethod
    def list(cls):
        return WidgetRegistry.widgets.keys()

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

    def render(self, field, state, **kw):
        """ Here is should be field rendering
        """
        # XXX: надо как-то пробрасывать сюда окружение, подробнее http://jinja.pocoo.org/docs/api/
        tmplt = FileSystemLoader('./templates/').get_template(self.template)
        return tmplt.render(field, state, **kw)

class TextWidget(Widget):
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
    name = 'textwidget'
    template = 'templates/widgets/textinput.html'
    size = None
    strip = True
    placeholder = ''
    tagtype = 'text'
    alter_names = ('text',)

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

class WYSIWYGWidget(Widget):
    name = 'wysiwyg'
    template = 'templates/widgets/wysiwyg.html'
    size = None
    strip = False
    placeholder = ''

    def serialize(self, field, cstruct, state):
        raise NotImplemented

    def deserialize(self, field, pstruct):
        raise NotImplemented

