__all__ = ['ConnectionError', 'connect', 'register_connection',
           'DEFAULT_DATASOURCE_NAME']

DEFAULT_DATASOURCE_NAME = 'default'

class ConnectionError(Exception):
    pass


_datasources = {}

def register_datasource(ds, connection, alias=DEFAULT_DATASOURCE_NAME, **kwargs):
    global _connection_settings
    ds_connection = ds(connection=connection, **kwargs)
    _connection_settings[alias] = ds_connection

def disconnect(alias=DEFAULT_DATASOURCE_NAME):
    global _datasources

    if alias in _datasources:
        get_connection(alias=alias).disconnect()
        del _datasources[alias]

def get_datasource(alias=DEFAULT_DATASOURCE_NAME, reconnect=False):
    global _datasources
    return _datasources[alias]
