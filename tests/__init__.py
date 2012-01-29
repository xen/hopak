from formgear.models import Model, ModelRegistry
from formgear.fields import FieldsRegistry
import logging
import yaml


def field_comparison_helper(collect_field_classes, source_yaml):

    for field in source_yaml['fields']:
        field_class = FieldsRegistry.resolve(field.pop('type', 'string').lower())
        assert field_class in collect_field_classes
        collect_field_classes.remove(field_class)


def test():

    class User(Model):
        __yaml__ = 'doctype'

    assert ['user',] == ModelRegistry.list()

    class Order(Model):
        __yaml__ = 'order'

    # testing ModelRegistry completion
    assert ['user', 'order'] == ModelRegistry.list()

    user = User()
    user_yaml = yaml.safe_load(open(User.__yaml__))
    user_field_classes = [type(model_field[1]) for model_field in user._fields]
    # testing field creation
    field_comparison_helper(user_field_classes, user_yaml)

    order = Order()
    order_yaml = yaml.safe_load(open(Order.__yaml__))
    order_field_classes = [type(model_field[1]) for model_field in order._fields]
    # testing field creation
    field_comparison_helper(order_field_classes, order_yaml)

