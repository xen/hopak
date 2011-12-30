# -*- coding: utf-8 -*-
#

__author__ = 'xen'

class WidgetRegistry(object):
    # XXX нужны методы отображения и поиска по реестру
    models = []

class MetaWidget(type):
    """
    Class for all widgets
    """
    def __new__(cls, name, bases, attrs):
        print("Register new widget:", cls)
        print("Class bases:", bases)
        print("Class name:", name)
        print("Class attrs", attrs)

        # register models in global list
        WidgetRegistry.models.append(cls)

        return super(MetaWidget, cls).__new__(cls, name, bases, attrs)

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

    template = 'textinput'
    size = None
    strip = True
    placeholder = ''
    tagtype = 'text'

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

