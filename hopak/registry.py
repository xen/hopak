class NotFoundException(Exception):
    pass

class DublicateRegistryEntryException(Exception):
    pass

class Registry(object):
    """ Registry is singleton wich maintain list of registered classes and
    allow to quick resolve into class by simple key search.

    >>> from hopak.registry import Registry, NotFoundException
    >>> class NotFoundTestException(Exception):
    ...     pass
    ...

    Sample class

    >>> class TestRegistry(Registry):
    ...     NotFound = NotFoundTestException
    ...
    >>> type(TestRegistry)
    <class 'hopak.registry.__metaclass__'>

    >>> assert isinstance(TestRegistry, object)

    Actual usage example

    >>> class TestObject(object):
    ...     alter_names = ('test1', 'test2', )
    ...
    >>> TestRegistry.register(TestObject, 'testobject')
    >>> TestRegistry.resolve('testobject')
    <class 'hopak.registry.TestObject'>
    >>> TestRegistry.resolve('test1')
    <class 'hopak.registry.TestObject'>

    Exception example if item is not found

    >>> TestRegistry.resolve('test_notfound')
    Traceback (most recent call last):
    ...
    NotFoundTestException: Key 'test_notfound' not found in <class 'hopak.registry.TestRegistry'>

    Resolved item is the same as original class

    >>> TestObject == TestRegistry.resolve('testobject')
    True

    Whole registry contains all name variations

    >>> TestRegistry.list()
    ['test1', 'test2', 'testobject']

    >>> TestRegistry.unregister('test2')
    >>> TestRegistry.list()
    ['test1', 'testobject']


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
    def lookup(cls, name):
        """ le Check da existence """
        return cls.data.has_key(name)

    @classmethod
    def register(cls, val, name):
        for x in getattr(val, 'alter_names', []):
            if not cls.data.has_key(x):
                cls.data[x] = val
            else:
                raise DublicateRegistryEntryException

        cls.data[name] = val

    @classmethod
    def unregister(cls, what):
        """ Remove items from registry """
        if type(what) == str:
            del cls.data[what]
        elif type(what) == list:
            for i in what:
                assert type(i) == str
                del cls.data[i]
        else:
            # some duck typing
            for i in getattr(what, 'alter_names', []):
                del cls.data[i]

    @classmethod
    def list(cls):
        return cls.data.keys()
