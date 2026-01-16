import json
import os
from typing import List
from coinrule_x_indicators.core import CandleData

def load_candles(filename: str = "candles.json") -> List[CandleData]:
    """
    Load candles from a JSON file in the tests/data directory.
    
    The JSON structure is expected to be a list of dicts with keys:
    s: symbol
    i: interval
    o: open
    h: high
    l: low
    c: close
    v: volume
    n: number of trades
    t: timestamp (open time)
    T: close time
    """
    # Determine the path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', filename)
    
    with open(data_path, 'r') as f:
        data = json.load(f)
        
    candles = []
    for entry in data:
        candles.append(CandleData(
            timestamp=entry['t'],
            open=float(entry['o']),
            high=float(entry['h']),
            low=float(entry['l']),
            close=float(entry['c']),
            volume=float(entry['v'])
        ))
        
    return candles
