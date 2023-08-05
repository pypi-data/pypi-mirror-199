# Importing external libraries
import unittest
import sys

# Importing libraries we want to test
sys.path.append('../../')
import src.gqpy.gqpy as gq
from tests import Tests

class TestBitfinexLive(unittest.TestCase):

    def setUp(self):

        self.tests = Tests()
        self.exchange = gq.GoQuant().exchanges.Bitfinex

    def test_ticker(self):

        self.tests.ticker(self.exchange, ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_ticker_multiple_pairs(self):

        self.tests.ticker(self.exchange, ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

    def test_trade(self):

        self.tests.trade(self.exchange, ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_trade_multiple_pairs(self):

        self.tests.trade(self.exchange, ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

    def test_book(self):

        self.tests.book(self.exchange, ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_book_multiple_pairs(self):

        self.tests.book(self.exchange, ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

if __name__ == "__main__":
    unittest.main()