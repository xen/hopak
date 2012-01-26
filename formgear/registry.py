class NotFoundException(Exception):
    pass

class Registry(object):
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
