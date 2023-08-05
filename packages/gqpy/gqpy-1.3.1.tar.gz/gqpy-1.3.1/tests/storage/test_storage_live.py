# Importing external libraries
import sys, unittest, os
from pymongo import MongoClient

# Importing libraries we want to test
sys.path.append('../../')
import src.gqpy.gqpy as gq

class TestStaticStorage(unittest.TestCase):

    def setUp(self):

        self.gq = gq.GoQuant()

    def test_csv(self):

        path_to_file = 'test_csv_live.txt'

        csv_ctx = self.gq.storage.CsvStorageContext(path_to_file)
        self.gq.live.ticker('binance', ['btcusdt', 'ethbtc', 'ltcbtc'], False, 10, csv_ctx)

        # Reading the file
        f = open(path_to_file, "r")
        content = f.read()
        self.assertTrue(len(content) > 0)
        f.close()

        self.assertTrue(f'binance.spot.ticker.BTCUSDT' in content or f'binance.spot.ticker.ETHBTC' in content or f'binance.spot.ticker.LTCBTC' in content)

        if os.path.isfile(path_to_file):
            os.remove(path_to_file)

    def test_mongo(self):

        connection_uri = 'mongodb+srv://admin:1231@cluster0.fiusevn.mongodb.net/?retryWrites=true&w=majority'
        database_name = 'test'
        collection_name = 'btc_usdt_live'

        mongo_ctx = self.gq.storage.MongoStorageContext(connection_uri, database_name, collection_name)
        self.gq.live.ticker('binance', ['btcusdt', 'ethbtc', 'ltcbtc'], False, 5, mongo_ctx)

        client = MongoClient(connection_uri)
        db = client[database_name]
        col = db[collection_name]
        dp = col.find_one()

        self.assertEqual(dict, type(dp))
        self.assertEqual(dp['assetClass'], 'spot')
        self.assertTrue(dp['channel'] == 'binance.spot.ticker.BTCUSDT' or dp['channel'] == 'binance.spot.ticker.ETHBTC' or dp['channel'] == 'binance.spot.ticker.LTCBTC')

        col.delete_many({})




if __name__ == "__main__":
    unittest.main()