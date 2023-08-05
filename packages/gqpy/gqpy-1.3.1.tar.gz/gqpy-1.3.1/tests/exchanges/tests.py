import unittest
import sys
import random

# Importing libraries we want to test
sys.path.append('../../')
import src.gqpy.gqpy as gq

class Tests(unittest.TestCase):

    def ticker(self, exchange, input_symbol_pairs, output_symbol_pairs, print_res, time):

        gqpy = gq.GoQuant()

        res = gqpy.live.connect(gqpy.data_types.Ticker, exchange, input_symbol_pairs, print_res, time)

        # Ensuring the correct type was returned
        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        # Ensuring the correct format was returned
        dp = res[-1]
        self.assertEqual(dict, type(dp))

        # Checking to see if the response was in one of the channels (the user may request multiple)
        possible_channels = []
        for pair in output_symbol_pairs:
            possible_channels.append(f'{exchange}.spot.ticker.{pair}')

        # Picking five random data points to see if they are from the requested channels
        for i in range(5):
            rand = random.randint(0, len(res) - 1)
            self.assertEqual(res[rand]['assetClass'], 'spot')
            self.assertTrue(res[rand]['channel'] in possible_channels)
        
    def book(self, exchange, input_symbol_pair, output_symbol_pairs, print_res, time):
 
        gqpy = gq.GoQuant()

        res = gqpy.live.connect(gqpy.data_types.Book, exchange, input_symbol_pair, print_res, time)

        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        dp = res[-1]
        self.assertEqual(dict, type(dp))

        # Checking to see if the response was in one of the channels (the user may request multiple)
        possible_channels = []
        for pair in output_symbol_pairs:
            possible_channels.append(f'{exchange}.spot.book.{pair}')

        # Picking five random data points to see if they are from the requested channels
        for i in range(5):
            rand = random.randint(0, len(res) - 1)
            self.assertEqual(res[rand]['assetClass'], 'spot')
            self.assertTrue(res[rand]['channel'] in possible_channels)

    def trade(self, exchange, input_symbol_pair, output_symbol_pairs, print_res, time):

        gqpy = gq.GoQuant()

        res = gqpy.live.connect(gqpy.data_types.Trade, exchange, input_symbol_pair, print_res, time)

        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        dp = res[-1]
        self.assertEqual(dict, type(dp))

        # Checking to see if the response was in one of the channels (the user may request multiple)
        possible_channels = []
        for pair in output_symbol_pairs:
            possible_channels.append(f'{exchange}.spot.trade.{pair}')

        # Picking five random data points to see if they are from the requested channels
        for i in range(5):
            rand = random.randint(0, len(res) - 1)
            self.assertEqual(res[rand]['assetClass'], 'spot')
            self.assertTrue(res[rand]['channel'] in possible_channels)