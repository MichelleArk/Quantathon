class Overnight(Strategy):
    
    def __init__(self):
        pass
    
    def execute(self, state):
        global funds
        #1
        calculate_interest(funds)
        #2
        profit_loss()
        #3
        pipeline_decisions()
        #4
        super(Strategy, self).sell_to_refinery(10000, state.oil_spot)
        #5
        future_prediction = get_future_prediction()
        future_decision(future_prediction)
        #6
        check_debt(state.oil_spot)
        #7
        confirm_exposure()

    def calculate_interest():
        global funds
        funds = (funds * 0.008) - (borrowed * 0.01)
    
    #KATHY      
    def profit_loss():
        pass
    
    def check_debt(oil_spot):
        if borrowed > 0.5*oil_spot*oil_holdings:
          
            oil_holdings = oil_spot*barrels
            to_sell = funds - 0.5*oil_holdings
          
        if sell < 30000:
            sell_to_pipeline(to_sell, oil_spot)
        else:       
    
    def confirm_exposure(oil_spot, oil_futures):
        exposure = barrels + futures
        if exposure <= 1:
            super(Strategy, self).purchase_from_pipeline((-1) * exposure + 1)
        elif exposure >= 1000000:
            if oil_spot * barrels >= oil_futures * future_barrels:
                super(Strategy, self).sell_to_pipeline(barrels, oil_spot)
            else:
                super(Strategy, self).sell_futures(future_barrels, oil_futures)
    
    #STEPAN
    def future_decision(prediction):
        #WRITE THIS
        pass

    #MICHELLE
    def pipeline_decision():
        #WRITE THIS
        pass