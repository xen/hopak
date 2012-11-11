# -*- coding: utf-8 -*-
#
from .base import BaseDS

class MongoDS(BaseDS):
    """ Mongodb Data Source
    """

    def __init__(self, connection, collection):
        self.conn = connection
        self.collection = db[collection]

    def save(self, id):
        _id = _id or data.get('_id')
        if not (_id is None):
            self.collection.update({"_id": _id}, data, upsert=True, safe=True)
            return _id
        else:
            return self.collection.insert(data)

    def get(self, id):
        return self.collection.find({"_id": _id})

    def delete(self, id):
        self.collection.remove({"_id": _id})

    def save_multi(self, ids=[]):
        pass

    def get_multi(self, ids=[]):
        pass

    def delete_multi(self, ids=[]):
        pass

    def find(collection, **kw):
        return self.collection.find(kw)

    def count(self, **kw):
        return self.collection.count(kw)

    def disconnect(self):
        self.conn.disconnect()

