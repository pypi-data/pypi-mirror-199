# TODO: Remove this file, symbol exchange calls have been moved to the API

# Importing external libraries
import requests

def binance():

        # Getting exchange info from Binance's public API endpoint
        res = requests.get('https://api.binance.com/api/v3/exchangeInfo')
        symbol_pair_list = res.json()['symbols']
        
        symbols = []
        for symbol in symbol_pair_list:
            symbols.append(symbol['symbol'].lower())

        return symbols

def bitfinex():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.bitfinex.com/v1/symbols_details')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        if ':' not in symbol['pair']: symbols.append(symbol['pair'].lower())

    return symbols

def bitstamp():

    res = requests.get('https://www.bitstamp.net/api/v2/trading-pairs-info/')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['url_symbol'].lower())

    return symbols

def bybit():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.bybit.com/derivatives/v3/public/instruments-info')
    symbol_pair_list = res.json()['result']['list']
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['symbol'].lower())

    return symbols

def coinbase():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.exchange.coinbase.com/products/')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['id'].lower())

    return symbols

def huobi():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.huobi.pro/v1/common/symbols')
    symbol_pair_list = res.json()['data']

    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['symbol'].lower())

    return symbols

def okex():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://www.okx.com/api/v5/public/instruments?instType=SPOT')
    symbol_pair_list = res.json()['data']

    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['instId'].lower())

    return symbols