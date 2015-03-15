import settings
import numpy as np

class Strategy(object):
    
    def __init__(self):
        pass
    
    def calculate_interest(self):
        settings.funds = (settings.funds * 0.008) - (settings.borrowed * 0.0001)

    def get_curve(self, price_points):
        y = np.array(price_points)
        time = [i for i in range(len(y))]
        x = np.array(time)
        
        f = []
        rsquared = []
        for i in range(3):
            fi = np.polyfit(x, y, i)
            f.append(fi)
            p = np.poly1d(fi)
            yhat = p(x)
            ybar = np.sum(y)/len(y)
            ssreg = np.sum((yhat-ybar)**2)
            sstot = np.sum((y - ybar) ** 2)
            if sstot == 0:
                rsquared.append((1, i))
            else:
                rsquared.append((ssreg / sstot, i))
        #check that we don't get overfitting
        best_r = rsquared[0]
        best_i = 0
        for i in range(len(rsquared)):
            if best_r < rsquared[i]:
                best_i = i
            else:
                pass
        
        return f[best_i]
    
    def get_predictions(self, price_points, index):
        
        value = 0
        f = self.get_curve(price_points)
        for i in range(len(f)):
            value += f[i] * ((index) ** i)
        return value
    
    #KATHY      
    def profit_loss(self, state, pipeline_prediction):
        pl = pipeline_prediction - state.oil_futures - state.oil_futures_rs
        settings.funds += pl * (settings.future_barrels*state.oil_futures)
        
        return pl
    
    def check_debt(self, oil_spot):
        oil_holdings = oil_spot*settings.barrels 
        if settings.borrowed > 0.5*oil_holdings:          
            to_sell = settings.borrowed - 0.5*oil_holdings / oil_spot
          
            if to_sell < 30000:
                self.sell_to_pipeline(to_sell, oil_spot)
                settings.borrowed -= to_sell*oil_spot
            else:
                self.sell_to_pipeline(30000, oil_spot)
                settings.borrowed -= 30000*oil_spot
    
    def confirm_exposure(self, oil_spot, oil_futures):
        
        exposure = settings.barrels + settings.future_barrels
        if exposure <= 1:
            self.purchase_from_pipeline((-1) * exposure + 1, oil_spot)
        elif exposure >= 1000000:
            if oil_spot * settings.barrels >= oil_futures * settings.future_barrels:
                self.sell_to_pipeline(settings.barrels, oil_spot)
            else:
                self.sell_futures(settings.future_barrels, oil_futures)
    
    def sell_to_pipeline(self, num_barrels, oil_spot):
        settings.funds = settings.funds + (oil_spot * num_barrels * 0.99)
        settings.barrels = settings.barrels - num_barrels
        
    def purchase_from_pipeline(self, num_barrels, oil_spot):
        if num_barrels > 60000:
            settings.funds = settings.funds - (oil_spot * 30000)
            settings.funds = settings.funds - (oil_spot * 30000 * 1.01)
            settings.barrels = settings.barrels + 60000
        elif num_barrels > 30000:
            settings.funds = settings.funds - (oil_spot * 30000)
            settings.funds = settings.funds - (oil_spot * (num_barrels - 30000) * 1.01)
            settings.barrels = settings.barrels + num_barrels
        else:
            settings.funds = settings.funds - (oil_spot * num_barrels)
            settings.barrels = settings.barrels + num_barrels
            
    def sell_to_refinery(self, num_barrels, oil_spot):
        settings.funds = settings.funds + (num_barrels * oil_spot)
        settings.barrels = settings.barrels - num_barrels            
        
        
    def buy_futures(self, num_fbarrels, oil_futures):
        settings.future_barrels += num_fbarrels
        settings.funds -= num_fbarrels * oil_futures - (0.05 * oil_futures)
        
    def sell_futures(self, num_fbarrels, oil_futures):
        settings.future_barrels -= num_fbarrels
        settings.funds += num_fbarrels * oil_futures - (0.05 * oil_futures)
    
    def check_funds(self, necessary):
        if settings.funds < neccesary: 
            borrow(necessary - settings.funds)
    
    def borrow(amount):
        settings.borrowed = settings.borrowed + amount
        
