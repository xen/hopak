from pymongo import Connection

connection = Connection()
db = connection['comfortly']

def save(collection, data):
    col = db[collection]
    if '_id' in data:
        col.update({"_id": data['_id']}, data, upsert=True, safe=True)
    else:
        col.insert(data)

def find(collection, **kw):
    col = db[collection]

    return col.find(kw)

def remove(collection, _filter):
	col = db[collection]
	print collection, _filter
	col.remove(_filter)