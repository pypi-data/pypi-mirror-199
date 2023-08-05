# Importing external dependencies
import sys

# Importing internal classes
from ..storage import Storage

def store_to_csv(csv_obj=Storage.CsvStorageContext(None), data=None):
    
    original_stdout = sys.stdout

    with open(csv_obj.file_location, 'a') as f:
        sys.stdout = f
        print(data + ',')
        sys.stdout = original_stdout