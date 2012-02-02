# formgear

**Внимание, код не является полностью работающим, но является прототипом. Цель публикации документации — привлечь внимание**

formgear — это активно развиваемый проект идея которого в том, чтобы максимально упростить работу по созданию сайтов.
Когда планирую сайт, то делаю его в несколько простых этапов. Перый - это подготовка чего-то типа "карты сайта". Обычно
назваю этот документ `sitemap.txt`. Пример такого документа:

```
- Главная страница
- Новости
  - Страница новости
  - Архив
- О нас
- Форма заказа
```

После этого приступаю к формированию списков типов контента на сайте, например в примере выше видно, что есть
приблизительно такой список:

- Новость
- Страница текста (скорее всего страница "О нас")
- Форма заказа

Расписав каждый тип данных приблизительно в таком виде, можно понять какие структуры данных будут. Вот пример описания
Новости:

- Название (строка)
- Краткий текст
- slug
- Тело новости
- Картинка

Как программисту кажется, что такого описания уже должно быть достаточно чтобы нажать какую-то магическую кнопку и
получить работающий сайт. Для этого и создается **formgear**. Взять какой-то простой и предсказуемый синтаксис
(никакого сраного XML) и сделать так чтобы после создания документов все магическим образом заработало.

На данный момент в проекте уже реализовано создание моделей в очень простом декларативном стиле, либо с помощью
python кода, либо с помощью YAML описания близкого по формату к обычному тексту (чуть более в формализированном виде).

Вот пример того как можно создать модель, файл news.yaml:

```yaml
title: News Page
description: >
  News page that appears on the site. Here is description for admin section. Hope
  you enjoy this simple format.

fields:
  - name: title
    title: News Title
    type: string
    length: 80
    required: 1
  - name: leadin
    title: Lead description usually small version of body.
    type: string
    length: 80
    widget:
      name: textarea
      rows: 5
      css: bold
  - name: publishdate
    title: Publish Date
    type: date
    widget: date
  - name: body
    title: News item body
    description: >
      Some text about you here is welcome
    widget:
      name: markdownwysiwyg
      theme: simple
  - name: image
    type: image
    desription: >
      Main photo, will be autoresized
    widget:
      name: image
      addons: [crop, url]
```

Этот код не совсем актуальный, но дает представление о идее. Теперь самое главное, как же работать с этим файлом.
В текущий момент реализован следующий путь:

```python
from formgear.models import Model
class NewsYAML(Model):
  __yaml__ = 'news.yaml'
  # тут код который вы хотите использовать дополнительно
  # он может прекрывать определения из yaml файла

# этот код эквивалентен приблизительно следующему python коду

from formgear.fields import *
from formgear.widgets import *

class NewsPy(Model):
  title = StringField(title="News Title", length=80, required=True)
  leadin = StringField(title="Lead...", length=80, widget=TextareaWidget(rows=5, css='bold'))
  publishdate = DateTimeField(...)
  body = TextField(...)
  # etc, думаю идея понятна

# код можно совмещать, например если вы решили создать дополнительное свойство
# не в yaml файле, а в python коде

class NewsMix(Model):
  __yaml__ = 'news.yaml'
  popular = BooleanField(title="Popular news", default=False)

# теперь надо попробовать сгеренировать форму:

killallhumans = NewsMix(...)

for field in killallhumans.form():
  print field()

# этот код вернет HTML код для отображения формы.
```

TODO:

- В текущий момент модели пока не умеют хранить данные
- API могут меняться, особенно в части с импортом моделей и виджетов
  уже есть реестры, но хочется сильно упростить описательную часть
- пока нет url роутингов, но пример идеи можно посмотреть в `test/data/sample/sitemap.yaml`
- не понятно будет ли этот проект оформлен как библиотека которую можно будет использовать
  в любых своих проектах или будет тесно связан с каким-то фреймворком
- formgear дурацкое название, скорее всего будет придумано какое-то более эпичное
- нет вообще никаких тестов
