# -*- coding: utf-8 -*-
#

class BaseDS(object):
    """ Data source interface
    """

    def __init__(self, conn):
        self.conn = conn

    def save(self, id):
        raise NotImplemented

    def get(self, id):
        raise NotImplemented

    def delete(self, id):
        raise NotImplemented

    def save_multi(self, ids=[]):
        raise NotImplemented

    def get_multi(self, ids=[]):
        raise NotImplemented

    def delete_multi(self, ids=[]):
        raise NotImplemented

    def query(self):
        raise NotImplemented

    def count(self):
        raise NotImplemented

    def disconnect(self):
        raise NotImplemented

