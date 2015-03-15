import csv, main, settings
from baseline import Baseline 
from strategy import Strategy 
from ourstrategy import ourStrategy
from state import State 


if __name__ == "__main__":
    
    settings.init()
    startDate = 20050103
    i_r = 0
    i_s = 0
    
    file1 = open("in_sample.csv")
    #Create csv file object
    csv_f = csv.reader(file1)

    result = open("baseline_in_sample.csv", 'w')
    csv_r = csv.writer(result, quoting=csv.QUOTE_ALL)
    
    result_s = open("strategy_out_sample.csv",'w')
    csv_s = csv.writer(result_s, quoting = csv.QUOTE_ALL)
    
    header = ["Date", "Barrels bought or sold", "Futures contracts bought or sold", "Barrels after overnight", "Cash after overnight", "Futures(in barrels) after overnight", "Debt / Oil Holdings", "Profit & Loss", "oil_spot forecast", "oil_futures forecast"]
    csv_r.writerow(header)
    
    for row in csv_f:
        if i_r == 0:
            pass
            i_r +=1
 
        else:
            state_today = State(row)
            baseline = Baseline()
            
            barrels_init = settings.barrels
            futures_init = settings.future_barrels
            
            result_l = [0 for x in range(10)]
            #Insert the date.
            result_l[0] = state_today.date
            
            #this is so that by the start date, we have data to use for a 
            #moving average analysis.
            settings.oil_prices.append(state_today.oil_spot)
            settings.future_prices.append(state_today.oil_futures)
            #also need to call method that will calculate forecasts, and insert the into header. 
            
            if int(row[0]) < startDate:
                oil_forecast = super(Baseline, baseline).get_predictions(settings.oil_prices, len(settings.oil_prices))
                future_forecast = super(Baseline, baseline).get_predictions(settings.future_prices, len(settings.future_prices))
                result_l[8] = oil_forecast
                result_l[9] = future_forecast
                csv_r.writerow(result_l)
                continue            

            state_today.executeStrategy(baseline)

            result_l[1] = settings.barrels - barrels_init
            result_l[2] = settings.future_barrels - futures_init
            
            #Barrels after overnight
            result_l[3] = settings.barrels
        
            #Cash after overnight
            result_l[4] = settings.funds            
            result_l[5] = settings.future_barrels
            result_l[6] = settings.borrowed / state_today.oil_spot * settings.barrels
            result_l[7] = settings.strategy_decisions[0]
            result_l[8] = settings.strategy_decisions[1]
            result_l[9] = settings.strategy_decisions[2]

            #PRINT TO RESULTING CSV FILE
            csv_r.writerow(result_l)
    
    file1.close()
    file2 = open("in_sample.csv")
    #Create csv file object
    csv_f2 = csv.reader(file2)    

    for row in csv_f2:
        if i_s == 0:
            csv_s.writerow(header)
            i_s +=1
 
        else:
            state_today = State(row)
            our_strategy = ourStrategy()
            
            barrels_init = settings.barrels
            futures_init = settings.future_barrels
            
            result_l = [0 for x in range(10)]
            #Insert the date.
            result_l[0] = state_today.date
            
            #this is so that by the start date, we have data to use for a 
            #moving average analysis.
            settings.oil_prices.append(state_today.oil_spot)
            settings.future_prices.append(state_today.oil_futures)
            #also need to call method that will calculate forecasts, and insert the into header. 
            
            if int(row[0]) < startDate:
                oil_forecast = super(ourStrategy, our_strategy).get_predictions(settings.oil_prices, len(settings.oil_prices))
                future_forecast = super(ourStrategy, our_strategy).get_predictions(settings.future_prices, len(settings.future_prices))
                result_l[8] = oil_forecast
                result_l[9] = future_forecast
                csv_s.writerow(result_l)
                continue            

            state_today.executeStrategy(our_strategy)

            result_l[1] = settings.barrels - barrels_init
            result_l[2] = settings.future_barrels - futures_init
            
            #Barrels after overnight
            result_l[3] = settings.barrels
        
            #Cash after overnight
            result_l[4] = settings.funds          
            result_l[5] = settings.future_barrels
            result_l[6] = settings.borrowed / state_today.oil_spot * settings.barrels
            result_l[7] = settings.strategy_decisions[0]
            result_l[8] = settings.strategy_decisions[1]
            result_l[9] = settings.strategy_decisions[2]

            #PRINT TO RESULTING CSV FILE
            csv_s.writerow(result_l)
    

    result.close()
    result_s.close()
    file2.close()


