# Internal libraries
import requests

class Symbols():

    def get(self, exchange_name):

        res = requests.get(f'https://api.goquant.io/symbols?exchange={exchange_name}')
        res = res.text[1:-1].split(',')
        res = [i.replace('"', '', 2) for i in res]
        return res
