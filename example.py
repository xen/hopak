# -*- coding: utf-8 -*-
#

__author__ = 'xen'

from formgear.models import Model, ModelRegistry
from mongoengine import Document, StringField

class User(Model):
    __yaml__ = 'doctype'

john = User()


class Order(Model):
    __yaml__ = 'order'


order = Order()

print order.render_form()