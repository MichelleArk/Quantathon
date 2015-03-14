import csv
from state.py import State

#global funds
funds = 0
#global barrels
barrels = 500000
#global borrowed
borrowed = 0
#global future_barrels
future_barrels = 0
#global points
oil_prices = []

def calculate_interest():
    global funds
    funds = (funds * 0.008) - (borrowed * 0.01)

def check_debt(oil_spot):
    if borrowed > 0.5 * oil_spot * oil_holdings:

        oil_holdings = oil_spot * barrels
        to_sell = funds - 0.5*oil_holdings

        if sell < 30000:
            sell_to_pipeline(to_sell, oil_spot)
        else:
            sell_to_pipeline(30000, oil_spot)

def confirm_exposure():
    exposure = barrels + futures
    assert (exposure >= 1 and exposure <= 1000000)

if __name__ == "__main__":
    i = 0
    
    file = open("in_sample_data.csv - in_sample_data.csv.csv")
    #Create csv file object
    csv_f = csv.reader(file)

    result = open("result.csv", 'w', newline = '')
    csv_r = csv.writer(result, quoting=csv.QUOTE_ALL)
    header = ["Date", "Barrels bought or sold", "Futures contracts bought or sold", "Barrels after overnight", "Cash after overnight", "Futures(in barrels) after overnight", "Debt / Oil Holdings", "Profit & Loss", "oil_spot forecast", "oil_futures forecast"]
    csv_r.writerow(header)
    
    for row in csv_f:
        if i == 0:
            pass
            i +=1
        else:
        
            state_today = State(row)
            baseline = Baseline()
            overnight = Overnight()
            
            oil_prices.append(state_today.oil_spot)
        
            result_l = [z0 for x in range(10)]
            
            #Insert the date.
            result_l[0] = state_today.date
            
            state_today.executeStrategy(baseline)
            state_today.executeStrategy(overnight)

            #Barrels after overnight
            result_l[3] = barrels
        
            #Cash after overnight
            result_l[4] = funds
            #futures to # barrels?

            #PRINT RESULTING CSV FILE

            #fink this is right?: Barrels bought or sold
            #result_l[1] = row[1] - barrels
            csv_r.writerow(result_l)
    

    result.close()
    file.close()

