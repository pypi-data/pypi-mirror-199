# Importing external libraries
import requests

# Importing internal utility functions
from ..symbols.format import format_symbols
from ..storage.storage_utils import store_data



class Static:

    def __init__(self, url):
        self.url = url

    def ohlcv(self, exchange_name, symbol_pair, storage_obj=None):
        return handle_static_data(self.url, exchange_name, symbol_pair, 'ohlcv', storage_obj)

    def orderbook(self, exchange_name, symbol_pair, storage_obj=None):
        return handle_static_data(self.url, exchange_name, symbol_pair, 'orderbook_l2', storage_obj)

    def quote(self, exchange_name, symbol_pair, storage_obj=None):
        return handle_static_data(self.url, exchange_name, symbol_pair, 'quote', storage_obj)

    def trades(self, exchange_name, symbol_pair, limit, storage_obj=None):
        return handle_static_data(self.url, exchange_name, symbol_pair, 'trades', storage_obj, limit)

def handle_static_data(url, exchange_name, symbol_pair, data_type, storage_obj, limit=None):

    # Connecting to API V1
    connection_url = f'{url}api/static/{exchange_name}/spot?data_type={data_type}&symbol={symbol_pair.upper()}'

    if data_type == 'trades':
        connection_url += f'&limit={limit}'
    
    res = requests.get(connection_url).json()

    # If storage object is None, then the response is just returned
    if storage_obj:
        store_data(storage_obj, res)

    return res