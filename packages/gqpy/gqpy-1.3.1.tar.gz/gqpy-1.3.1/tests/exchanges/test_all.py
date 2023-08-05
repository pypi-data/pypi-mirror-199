# Importing external libraries
import unittest

# Importing libraries we want to test
from tests import Tests

class TestAllExchangesLive(unittest.TestCase):

    def setUp(self):
        
        self.tests = Tests()

    def test_binance(self):

        self.tests.ticker('binance', ['btcusdt'], 'BTCUSDT', False, 5)
        self.tests.book('binance', ['btcusdt'], 'BTCUSDT', False, 5)
        self.tests.trade('binance', ['btcusdt'], 'BTCUSDT', False, 5)

    def test_bitfinex(self):

        self.tests.ticker('bitfinex', ['BTCUSD'], 'tBTCUSD', False, 5)
        self.tests.book('bitfinex', ['BTCUSD'], 'tBTCUSD', False, 5)
        self.tests.trade('bitfinex', ['BTCUSD'], 'tBTCUSD', False, 5)

    def test_coinbase(self):

        self.tests.ticker('coinbase', ['BTC-USD'], 'BTC-USD', False, 5)
        self.tests.book('coinbase', ['BTC-USD'], 'BTC-USD', False, 5)
        self.tests.trade('coinbase', ['BTC-USD'], 'BTC-USD', False, 5)

    def test_kraken(self):

        self.tests.ticker('kraken', ['XBT/USD'], 'XBT/USD', False, 5)
        self.tests.book('kraken', ['XBT/USD'], 'XBT/USD', False, 5)
        self.tests.trade('kraken', ['XBT/USD'], 'XBT/USD', False, 5)

if __name__ == "__main__":
    unittest.main()