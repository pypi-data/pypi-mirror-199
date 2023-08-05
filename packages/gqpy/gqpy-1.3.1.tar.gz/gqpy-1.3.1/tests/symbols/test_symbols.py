# Importing external libraries
import sys
import unittest

# Importing libraries we want to test
sys.path.append('../../')
import src.gqpy.gqpy as gq

class TestSymbols(unittest.TestCase):

    def setUp(self):
        self.gq = gq.GoQuant()

    def test_binance(self):

        self.get_symbols('binance')

    def test_bitfinex(self):

        self.get_symbols('bitfinex')

    def test_coinbase(self):

        self.get_symbols('coinbase')

    def test_kraken(self):

        self.get_symbols('kraken')

    def get_symbols(self, exchange_name):

        res = self.gq.symbols.get(exchange_name)
        if exchange_name == 'kraken':
            print(res)
        self.assertTrue(type(res) == list and len(res) > 0) 



if __name__ == "__main__":
    unittest.main()