from strategy.py import Strategy
from state.py import State

class Baseline(Strategy):
    
    def __init__(self):
        pass
    
    def execute(self, state):
        global barrels
        sold_barrels = 0.1 * barrels
        super(Baseline, self).sell_to_pipeline(0.1 * barrels, state.oil_spot)
        super(Baseline, self).purchase_from_pipeline(10000, state.oil_spot)
        super(Baseline, self).buy_futures(0.5 * sold_barrels, state.oil_futures)
        super(Baseline, self).sell_to_refinery(10000, state.oil_spot)