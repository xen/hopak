# -*- coding: utf-8 -*-
#

__author__ = 'xen'

from formgear.models import Model #, ModelRegistry

class User(Model):
    __yaml__ = 'doctype'

john = User()

print john.render_form()

#class Order(Model):
#    __yaml__ = 'order'

#class All(Model):
#    __yaml__ = 'all'


#order = Order()
#print order.render_form()

#all = All()
#print all.render_form()