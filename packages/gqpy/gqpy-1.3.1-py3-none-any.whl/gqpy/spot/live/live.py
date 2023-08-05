# Importing internal functionality
from .handler import handle_live_data

class Live:

    def __init__(self, url):
        self.url = url

    def connect(self, data_type, exchange, symbol_pair, print=True, run_time=True, storage_obj=None):
        return handle_live_data(self.url, data_type, exchange, symbol_pair, print, run_time, storage_obj)