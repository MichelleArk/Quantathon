from strategy import Strategy
import numpy as np
import settings
from state import State

global prev_diff
prev_diff = 0

class ourStrategy(Strategy):
    
    def __init__(self):
        pass
    
    def execute(self, state):
        #1
        super(ourStrategy, self).calculate_interest()
        #2
        #Profit loss must return: the actual profit loss
        
        pipeline_prediction = super(ourStrategy, self).get_predictions(settings.oil_prices, len(settings.oil_prices))
        profit_loss = super(ourStrategy, self).profit_loss(state, pipeline_prediction)
        #3
        
        #p_decisions is an array, 0th element is 1 if buying, -1 if selling. 1st element is the number of barrels associated with decision

        p_decisions = self.pipeline_decision(pipeline_prediction, state.oil_spot)
	if p_decisions == 0:
	    sold_barrels = 0.1 * settings.barrels	
	    super(ourStrategy, self).sell_to_pipeline(sold_barrels, state.oil_spot)	    
	    super(ourStrategy, self).purchase_from_pipeline(10000, state.oil_spot)
	
        #4
        super(ourStrategy, self).sell_to_refinery(10000, state.oil_spot)
        #5
        future_prediction = super(ourStrategy, self).get_predictions(settings.future_prices, len(settings.future_prices))
	if p_decisions == 0:
	    super(ourStrategy, self).buy_futures(0.5 * sold_barrels, state.oil_futures)	
        else:
	    self.future_decision(profit_loss, p_decisions[0], p_decisions[1], future_prediction, state.oil_futures)
	
 	#6
        super(ourStrategy, self).check_debt(state.oil_spot)
        #7
        super(ourStrategy, self).confirm_exposure(state.oil_spot, state.oil_futures)
	
	settings.strategy_decisions[0] = profit_loss
	settings.strategy_decisions[1] = pipeline_prediction
	settings.strategy_decisions[2] = future_prediction	

    def future_decision(self, profit_loss, pipeline_decision, pipeline_amount, prediction, oil_futures):
	global barrels, future_barrels
	if pipeline_decision == -1: 
	    if profit_loss > oil_futures * 0.0005: #predicted profits per contract greater than transaction cost per contract
		super(ourStrategy, self).buy_futures(pipeline_amount, oil_futures) 
		settings.future_barrels += pipeline_amount
	    else:
		pass
	elif pipeline_decision == 1: #buying crude in the pipeline
	    if profit_loss < 0 and abs(profit_loss)>(oil_futures * 0.0005): #abs. value of predicted loss per contract is greater than transaction fee, therefore saving from losses  by shorting
		super(ourStrategy, self).sell_futures(pipeline_amount, oil_futures)
		settings.future_barrels -= pipeline_amount
	    else:
		pass

    def pipeline_decision(self, prediction, oil_spot):
        global prev_diff
        
        m20 = sum(settings.oil_prices[-20:])/20
        m120 = sum(settings.oil_prices[-120:])/120
        
        diff = m20 - m120
        tomorrow = prediction - oil_spot

        p_decision = []
        
        if (diff > 0) and (prev_diff < 0):
            p_decision.append(1)
            #Buy, prices are going up!
            if (tomorrow > 0) and (tomorrow > 0.5):
		print("buying aggressively")
                #buy a lot (x is a critical value, something high)
                super(ourStrategy, self).sell_to_pipeline(0.1*settings.barrels, oil_spot)
                p_decision.append(0.1*settings.barrels)
            else:
		print("buying conserv")
                super(ourStrategy, self).sell_to_pipeline(0.05*settings.barrels, oil_spot)
                p_decision.append(0.05*settings.barrels)
                
        elif (diff < 0) and (prev_diff > 0):
            p_decision.append(-1)
            #Sell, prices are going down
            if (tomorrow < 0) and (-1*tomorrow > 0.1):
		print("selling aggressively")
                #buy a lot, (y is a critical value, (make sure its neg), something really big
                super(ourStrategy, self).purchase_from_pipeline(0.1*settings.barrels, oil_spot)
                p_decision.append(0.1*settings.barrels)
            else:
		print("selling conserve")
                super(ourStrategy, self).purchase_from_pipeline(0.05*settings.barrels, oil_spot)
                p_decision.append(0.05*settings.barrels)
            
        if p_decision == []:
            p_decision.append(0)
            p_decision.append(0)
                
            #try to get second derivative of ma (short term) and predict concavity.
        
        prev_diff = diff
        
        return p_decision

        
        
