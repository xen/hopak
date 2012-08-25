from pymongo import Connection

connection = Connection()
db = connection['comfortly']

def save(collection, data, _id=None):
    col = db[collection]
    _id = _id or data.get('_id')
    if not (_id is None):
        col.update({"_id": _id}, data, upsert=True, safe=True)
        return _id
    else:
        return col.insert(data)

def find(collection, **kw):
    col = db[collection]

    return col.find(kw)

def remove(collection, _filter):
	col = db[collection]
	#print collection, _filter
	col.remove(_filter)
