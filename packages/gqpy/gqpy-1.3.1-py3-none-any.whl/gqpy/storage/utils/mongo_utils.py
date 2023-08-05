# Importing external dependencies
from pymongo import MongoClient
import json

# Importing internal libraries
from ..storage import Storage

def store_to_mongo(mongo=Storage.MongoStorageContext(None, None, None), data=None):
    
    doc = json.loads(data)

    client = MongoClient(mongo.query_string)
    db = client[mongo.database_name]
    col = db[mongo.collection_name]
    
    col.insert_one(doc)

    client.close()