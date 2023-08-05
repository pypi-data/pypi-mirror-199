# Importing external libraries
import websocket
import json
import time
import sys

# Importing internal utility functions
from ...storage.storage_utils import store_data

def handle_live_data(url, data_type, exchange, symbol_pairs, print_recv, run_time, storage_obj):

    ws = websocket.WebSocket()
    ws.connect(url)

    # Allowing multiple connections to be made
    for pair in symbol_pairs:
        connection_string = f'{{"event":"subscribe", "channel":"{exchange}.spot.{data_type}.{pair}"}}'
        ws.send(connection_string)

    start_time = time.time()
    cache = []

    while True:

        if type(run_time) != bool:

            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > run_time:
                # print(f'Data pipeline ran successfully and exited after {str(run_time)} seconds.')
                ws.close()
                return cache

        try:
            
            msg = ws.recv()
            
            # Checking to see if the symbol pair is supported
            if msg == '{"error":"Unsupported symbol pair."}':
                print(f'That symbol pair is not supported by {exchange}.')
                sys.exit(1)
            
            cache.append(json.loads(msg))

            if storage_obj:
                store_data(storage_obj, msg)
            elif print_recv:
                print(json.loads(msg))

        except KeyboardInterrupt:

            ws.close()
            break