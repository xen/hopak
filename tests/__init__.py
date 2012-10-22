from __future__ import absolute_import
from formgear.models import Model, ModelRegistry
from formgear.fields import FieldsRegistry
import logging
import yaml

import tests.models

def field_comparison_helper(collect_field_classes, source_yaml):

    for field in source_yaml['fields']:
        field_class = FieldsRegistry.resolve(field.pop('type', 'string').lower())
        assert field_class in collect_field_classes
        collect_field_classes.remove(field_class)


def test_lookup_class_by_yaml_attribute():

    class User(Model):
        __yaml__ = 'test_user'

    assert ['user',] == ModelRegistry.list()

    user = User()
    user_yaml = yaml.safe_load(open(User.__yaml__))
    user_field_classes = [type(model_field[1]) for model_field in user._fields]
    # testing field creation
    field_comparison_helper(user_field_classes, user_yaml)


def test_lookup_class_by_class_name():
    class Order(Model):
        __yaml__ = "test_order"
        pass

    # testing ModelRegistry completion
    assert ['user', 'order'] == ModelRegistry.list()

    order = Order()
    order_yaml = yaml.safe_load(open(Order.__yaml__))
    order_field_classes = [type(model_field[1]) for model_field in order._fields]
    # testing field creation
    field_comparison_helper(order_field_classes, order_yaml)
