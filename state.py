import settings

class State(object):
    
    def __init__(self, row):
        ''' Initialize the state.'''
        
        self.date = float(row[0])
        self.oil_spot = float(row[1])
        self.oil_futures = float(row[2])
        self.oil_futures_rs = float(row[3])
        self.commodities = row[4:]
        self.ma_20 = None
        self.ma_120 = None
        
    def executeStrategy(self, strategy):
        strategy.execute(self)
