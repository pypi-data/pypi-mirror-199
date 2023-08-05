# TODO: Remove this file, it is no longer used for symbol normalization

# Importing external libaraies
import sys

# Importing internal utility functions
from .requests import binance, bitfinex, bitstamp, bybit, coinbase, huobi, okex



def get_symbols(exchange_name):

    exchange_name = exchange_name.lower()
    symbols = []

    match exchange_name:
        case 'binance':
            symbols = binance()
        case 'bitfinex':
            symbols = bitfinex()
        case 'bitstamp':
            return bitstamp()
        case 'bybit':
            symbols = bybit()
        case 'coinbase':
            symbols = coinbase()
        case 'huobi':
            symbols = huobi()
        case 'okex':
            symbols = okex()

    return clean_symbols(symbols)
    
def clean_symbols(available_symbols):

    clean_list = []
    for s in available_symbols:

        # All symbol pairs will be standardized to the following format: aaabbb
        clean_list.append(s.lower().replace('-', '').replace('/', '').replace(' ', ''))

    return clean_list

def format_symbols(exchange_name, symbol_1, symbol_2):

    symbol_1 = symbol_1.lower()
    symbol_2 = symbol_2.lower()

    available_symbols = get_symbols(exchange_name)

    # Exchanges with dashed format (aaa-bbb)
    dashed_format = ['coinbase']

    # Exchanges with slashed format (aaa/bbb)
    slashed_format = ['kraken']

    # Exchanges with no dash
    regular_format = ['binance', 'bitfinex']

    # Getting the seperator for the exchange
    seperator = None
    if exchange_name in dashed_format:
        seperator = '-'
    elif exchange_name in slashed_format:
        seperator = '/'
    elif exchange_name in regular_format:
        seperator = ''
    else:
        print("The exchange entered is not a supported exchange.")
        sys.exit(1)

    # Bitfinex uses USD instead of USDT
    if exchange_name == 'bitfinex' and symbol_1.lower() == 'usdt':
        symbol_1 = 'usd'
    elif exchange_name == 'bitfinex' and symbol_2.lower() == 'usdt':
        symbol_2 = 'usd'

    symbol_pair = ''

    # Concatenating the two symbol pairs
    if symbol_1 + symbol_2 in available_symbols:
        symbol_pair = symbol_1 + seperator + symbol_2
    elif symbol_2 + symbol_1 in available_symbols:
        symbol_pair = symbol_2 + seperator + symbol_1
    else:
        print("That symbol pair is not supported by the specified exchange.")
        sys.exit(1)

    return symbol_pair