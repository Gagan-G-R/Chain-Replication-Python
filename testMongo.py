from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:27017/CRAQ"
client = MongoClient(CONNECTION_STRING)
db = client['CRAQ']

# insert
# ip = {'hello1': '1'}
# db['5201'].insert_one(ip)


# update
# query = {"hello": "world"}
# val = {"$set": {"hello": "world2"}}
# db['Node1'].update_one(query, val)


# # # read
# obj = db['Node2'].find_one({"_id": "hello"})
# print(obj['value'])


# find and update
query = {"_id": "gagan"}
val = {"$set": {"value": "3"}}
db["5201"].update_one(query, val, upsert=True)

# # list all collections
# collections = db.list_collection_names()
# no_of_collections = len(db.list_collection_names())
# result = {}
# for collection in collections:
#     obj = db[collection].find()
#     result[collection] = list(obj)
# print(result)
