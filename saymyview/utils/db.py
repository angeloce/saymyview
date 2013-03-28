#coding:utf-8

import types
import pymongo
from bson.dbref import DBRef


class MetaDocument(type):
    def __new__(cls, name, bases, attrs):
        for key in attrs:
            if not key.startswith('__') and isinstance(attrs[key], types.FunctionType):
                attrs[key] = classmethod(attrs[key])
        attrs.setdefault('_default_collection', name)
        attrs.setdefault('_default_db', 'painter')
        return type.__new__(cls, name, bases, attrs)

class Document(object):
    client = pymongo.MongoClient()
    __metaclass__ = MetaDocument
    _default_collection = 'temp'
    
    @property
    def collection(self):
        db = self.client[self._default_db]
        return db[self._default_collection]

    @property
    def dbref(self, docid):
        return DBRef(self._default_collection, docid, self._default_db)

    def find(self, **kwargs):
        return self.collection.find(kwargs)

    def find_one(self, **kwargs):
        return self.collection.find_one(kwargs)

    def insert(self, **kwargs):
        return self.collection.insert(kwargs)



