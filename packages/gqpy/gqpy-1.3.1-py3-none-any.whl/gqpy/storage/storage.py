class Storage():

    class CsvStorageContext():

        def __init__(self, file_location):
            self.file_location = file_location

    class MongoStorageContext():

        def __init__(self, query_string, database_name, collection_name):
            self.query_string = query_string
            self.database_name = database_name
            self.collection_name = collection_name