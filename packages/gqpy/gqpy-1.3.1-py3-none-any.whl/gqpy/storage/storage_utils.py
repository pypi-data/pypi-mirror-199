# Importing external dependencies
import sys

# Importing internal functions and classes
from .utils.csv_utils import store_to_csv
from .utils.mongo_utils import store_to_mongo
from .storage import Storage

def store_data(storage_obj, data):

    if isinstance(storage_obj, Storage.CsvStorageContext):
        store_to_csv(storage_obj, data)

    elif isinstance(storage_obj, Storage.MongoStorageContext):
        store_to_mongo(storage_obj, data)
        
    else:
        print("Your storage object (the last argument you pass to the live/static function) is not the correct type. It was of type " + type(storage_obj))
        sys.exit(1)