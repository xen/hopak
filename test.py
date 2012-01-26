# -*- coding: utf-8 -*-
#

__author__ = 'xen'

from formgear.models import Model, ModelRegistry
from mongoengine import Document, StringField

class User(Model):
    __yaml__ = 'test/data/doctype.yaml'

john = User()


class Order(Model):
    __yaml__ = 'test/sample/order.yaml'

class MOrder(Document):
    title = StringField()


order = Order()
morder = MOrder(title='Mongo orderzottsdf')
for field in order.form():
    print field('edit')

print ModelRegistry.list()