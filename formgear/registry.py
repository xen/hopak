class NotFoundException(Exception):
    pass

class Registry(object):
    """ Registry is singleton wich maintain list of registered classes an 
    allow to quick resolve into class by simple key search.

    >>> from formgear.registry import Registry, NotFoundException
    >>> class NotFoundTestException(Exception):
    ...     pass
    ... 

    Sample class 

    >>> class TestRegistry(Registry):
    ...     NotFound = NotFoundTestException
    ... 
    >>> type(TestRegistry)                            
    <class 'formgear.registry.__metaclass__'>

    >>> assert isinstance(TestRegistry, object)

    Actual usage example 

    >>> class TestObject(object):
    ...     alter_names = ('test1', 'test2', )
    ... 
    >>> TestRegistry.register(TestObject, 'testobject')
    >>> TestRegistry.resolve('testobject')
    <class 'formgear.registry.TestObject'>
    >>> TestRegistry.resolve('test1')
    <class 'formgear.registry.TestObject'>

    Exception example if item is not found

    >>> TestRegistry.resolve('test_notfound')
    Traceback (most recent call last):
    ...
    NotFoundTestException: Key 'test_notfound' not found in <class 'formgear.registry.TestRegistry'>

    Resolved item is the same as original class

    >>> TestObject == TestRegistry.resolve('testobject')
    True

    Whole registry contains all name variations

    >>> TestRegistry.list()
    ['test1', 'test2', 'testobject']


    """
    class __metaclass__(type):
        def __new__(cls, name, bases, attrs):
            data = attrs.get('data', {})
            attrs['data'] = data.copy()
            return type.__new__(cls, name, bases, attrs)

    data = {}

    @classmethod
    def resolve(cls, name, default=None):
        name = name.lower()
        if name in cls.data:
            return cls.data[name]
        elif default is not None:
            return default
        else:
            Exc = getattr(cls, 'NotFound', NotFoundException)
            raise Exc('Key %r not found in %r' % (name, cls))

    @classmethod
    def register(cls, val, name):
        # XXX: I'm not sure about that. Don't looks healthy
        for x in getattr(val, 'alter_names', []):
            cls.data[x] = val

        cls.data[name] = val

    @classmethod
    def list(cls):
        return cls.data.keys()
