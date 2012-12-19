from hopak.models import Model, ModelRegistry
from hopak.fields import FieldsRegistry
import yaml


def test_load_from_name():
    class ObjectFile(Model):
        # here is no __yaml__ attribute
        pass

    ModelRegistry.unregister(ObjectFile)
    del ObjectFile

def test_load_from_attribute():

    class ObjectYAML(Model):
        __yaml__ = 'object'

    ModelRegistry.unregister(ObjectYAML)
    del ObjectYAML


def test_load_from_attribute_ext():

    class ObjectYAML(Model):
        __yaml__ = 'object.yaml'

    ModelRegistry.unregister(ObjectYAML)
    del ObjectYAML


def test_load_lookup():

    class ObjectYAML(Model):
        __yaml__ = 'object'

    ModelRegistry.unregister(ObjectYAML)
    del ObjectYAML
