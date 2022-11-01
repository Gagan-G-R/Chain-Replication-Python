from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:27017/CRAQ"
client = MongoClient(CONNECTION_STRING)
db = client['CRAQ']

# insert
# ip = {'hello': '0'}
# db['Node2'].insert_one(ip)


# update
# query = {"hello": "world"}
# val = {"$set": {"hello": "world2"}}
# db['Node1'].update_one(query, val)


# # read
obj = db['Node2'].find_one({"_id": "hello"})
print(obj['value'])


# find and update
# query = {"_id": "gagan"}
# val = {"$set": {"value": "3"}}
# db["Node2"].update_one(query, val, upsert=True)
