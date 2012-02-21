# -*- coding: utf-8 -*-
#

class BaseDatasource(object):
    """ Data source interface
    """

    def __init__(self, conn):
        self.conn = conn

    def put(self):
        raise NotImplemented

    def get(self):
        raise NotImplemented

    def get_by_id(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented

    def put_multi(self):
        raise NotImplemented

    def get_multi(self):
        raise NotImplemented

    def del_multi(self):
        raise NotImplemented

    def query(self):
        raise NotImplemented

    def count(self):
        raise NotImplemented

    def commit(self):
        raise NotImplemented

    def rollback(self):
        raise NotImplemented
