import settings
from strategy import Strategy
from state import State

class Baseline(Strategy):
    
    def __init__(self):
        pass
    
    def execute(self, state):
        #1
        super(Baseline, self).calculate_interest()
        #2
        #Profit loss must return: the actual profit loss
        pipeline_prediction = super(Baseline, self).get_predictions(settings.oil_prices, state.oil_spot)        
        profit_loss = super(Baseline, self).profit_loss(state, pipeline_prediction)
        #3
        #p_decisions is an array, 0th element is 1 if buying, -1 if selling. 1st element is the number of barrels associated with decision
        sold_barrels = 0.1 * settings.barrels
        super(Baseline, self).sell_to_pipeline(0.1 * settings.barrels, state.oil_spot)
        super(Baseline, self).purchase_from_pipeline(10000, state.oil_spot)
        #4
        super(Baseline, self).sell_to_refinery(10000, state.oil_spot)
        #5
        future_prediction = super(Baseline, self).get_predictions(settings.future_prices, state.oil_futures)
        super(Baseline, self).buy_futures(0.5 * sold_barrels, state.oil_futures)
        #6
        super(Baseline, self).check_debt(state.oil_spot)
        #7
        super(Baseline, self).confirm_exposure(state.oil_spot, state.oil_futures)  
        
        settings.strategy_decisions[0] = profit_loss
        settings.strategy_decisions[1] = pipeline_prediction
        settings.strategy_decisions[2] = future_prediction
