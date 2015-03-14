class Strategy(object):
    
    def __init__(self):
        pass
    
    def sell_to_pipeline(self, num_barrels, oil_spot):
        global funds, barrels
        funds = funds + (oil_spot * num_barrels * 0.99)
        barrels = barrels - num_barrels
        
    def purchase_from_pipeline(self, num_barrels, oil_spot):
        global funds, barrels
        if num_barrels > 60000:
            funds = funds - (oil_spot * 30000)
            funds = funds - (oil_spot * 30000 * 1.01)
            barrels = barrels + 60000
        elif num_barrels > 30000:
            funds = funds - (oil_spot * 30000)
            funds = funds - (oil_spot * (num_barrels - 30000) * 1.01)
            barrels = barrels + num_barrels
        else:
            funds = funds - (oil_spot * num_barrels)
            barrels = barrels + num_barrels
            
    def sell_to_refinery(self, num_barrels, oil_spot):
        global funds, barrels
        funds = funds + (num_barrels * oil_spot)
        barrels = barrels - num_barrels            
        
        
    def buy_futures(self, num_fbarrels, oil_futures):
        global funds, future_barrels
        future_barrels += num_fbarrels
        funds -= num_fbarrels * oil_futures - (0.05 * oil_futures)
        
    def sell_futures(self, num_fbarrels, oil_futures):
        global funds, future_barrels
        future_barrels -= num_fbarrels
        funds += num_fbarrels * oil_futures - (0.05 * oil_futures)
        
    
        
    