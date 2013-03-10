# -*- coding: utf-8 -*-
#
from .base import BaseDS

class MongoDS(BaseDS):
    """ Mongodb Data Source
    """

    def __init__(self, conn):
        self.conn = conn

    def save(self, kind, data, _id=None):
        col = self.conn.db[kind]
        _id = _id or data.get('_id')
        if not (_id is None):
            col.update({"_id": _id}, data, upsert=True, safe=True)
            return _id
        else:
            return col.insert(data)

    def get(self, _id):
        return self.conn.db.find({"_id": _id})

    def remove(self, kind, fltr):
        self.conn.db[kind].remove(fltr)
    def save_multi(self, ids=[]):
        pass

    def get_multi(self, ids=[]):
        pass

    def delete_multi(self, ids=[]):
        pass

    def find(self, col, **kw):
        return self.conn.db[col].find(kw)

    def count(self, **kw):
        return self.conn.db.count(kw)

    def disconnect(self):
        self.conn.disconnect()

