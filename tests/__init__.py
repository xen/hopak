from formgear.models import Model, ModelRegistry

def test():
    class User(Model):
        __yaml__ = 'tests/test/data/doctype.yaml'

    class Order(Model):
        __yaml__ = 'tests/test/sample/order.yaml'
    
    print ModelRegistry.list()