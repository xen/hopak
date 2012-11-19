__all__ = ['ConnectionError', 'register_datasource',
    'get_datasource', 'DEFAULT_DATASOURCE_NAME']

DEFAULT_DATASOURCE_NAME = 'default'

class ConnectionError(Exception):
    pass

_datasources = {}

def register_datasource(ds, alias=DEFAULT_DATASOURCE_NAME):
    global _datasources
    _datasources[alias] = ds

def get_datasource(alias=DEFAULT_DATASOURCE_NAME):
    global _datasources
    return _datasources[alias]
