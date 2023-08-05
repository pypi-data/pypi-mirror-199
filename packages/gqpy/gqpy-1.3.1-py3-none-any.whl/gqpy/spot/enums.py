from enum import Enum

class Exchanges(Enum):

    Binance = 'binance'
    Bitfinex = 'bitfinex'
    Kraken = 'kraken'
    Coinbase = 'coinbase'

    def get_supported_exchanges():
        return ['binance', 'bitfinex', 'kraken', 'coinbase']
    
class DataTypes(Enum):

    Book = 'book'
    Ticker = 'ticker'
    Trade = 'trade'