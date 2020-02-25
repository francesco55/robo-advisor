# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from keyword import iskeyword
import plotly
import plotly.graph_objs as go

load_dotenv()

def to_usd(my_price):
    
    #Converts a numeric value to usd-formatted string, for printing and display purposes.
    #Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    #Param: my_price (int or float) like 4000.444444
    #Example: to_usd(4000.444444)
    #Returns: $4,000.44
    
    return f"${my_price:,.2f}"

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("This application gathers a company's recent stock data, stores the data in a CSV file, and outputs a recommendation for purchase.")
print("You may enter at most 5 stock tickers per minute.")
print("Enter the tickers one by one. Enter 'DONE' when you are finished entering tickers.")
print("Thank you!")


#adapted from shopping_cart.py
#multiple tickers input and validation

ticker_list = []
ticker_max = 5

#https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

while True:
    TICKER = input("Please enter a company's ticker: ")
    if TICKER.upper() == "DONE":
        break
    elif len(TICKER) > ticker_max or len(TICKER) < 1:
        print("This is not a valid ticker, it is an incorrect length.")
        print("Please enter a valid ticker.")
    elif hasNumbers(TICKER):
        print("This is not a valid ticker, it contains a number.")
        print("Please enter a valid ticker.")
    else:
        ticker_list.append(TICKER)

for TICKER in ticker_list:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={TICKER}&apikey={API_KEY}&outputsize=full"
    print("REQUESTING SOME DATA FROM THE INTERNET...")
    print("URL:", request_url)

    response = requests.get(request_url)

    #input validation

    if "Error Message" in response.text:
        print("ERROR")
        print(f"There is an error with either your inputted ticker ({TICKER}) or api key.")
        print("Please look into both and try again")
        print("___________________________________")
        continue

    if "higher API call frequency" in response.text:
        print("Error")
        print(response.text)
        exit()

    parsed_response = json.loads(response.text)
    #print(parsed_response)
    refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Time Series (Daily)"]

    date = list(tsd.keys()) #https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
    recent_close = tsd[str(date[0])]["4. close"]
    latest_date = date[0]


    #this and the following for loop creates lists parallel to the date list
    open_p = []
    high = []
    low = []
    close = []
    volume = []

    for d in date:
        current_open = float(tsd[d]["1. open"])
        open_p.append(current_open)
        current_high = float(tsd[d]["2. high"])
        high.append(current_high)
        current_low = float(tsd[d]["3. low"])
        low.append(current_low)
        current_close = float(tsd[d]["4. close"])
        close.append(current_close)
        current_volume = float(tsd[d]["5. volume"])
        volume.append(current_volume)

    #print(open_p)
    #print(high)
    #print(low)
    #print(close)
    #print(volume)

    #this code cuts the date variable into three variables
    #https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
    current_year = int(date[0][0:4]) 
    current_month = date[0][5:7]
    current_day = date[0][8:10]

    #this code finds the date a year ago today
    past_year = current_year - 1
    past_date = f"{str(past_year)}-{current_month}-{current_day}" #format
    
    #print(current_year)
    #print(type(current_month))
    #print(current_month)
    #print(current_day)
    #print(past_year)
    #print(past_date)

    #the following code checks if there is market data for the date exactly one year ago
    #if there is no market data one year ago exactly, the day prior is checked until a valid date is found
    while past_date not in date:
        if current_day == "01":
            if current_month == "11" or current_month == "12":
                current_month = str(int(current_month)-1)
            else:
                current_month = f"0{str(int(current_month) - 1)}"
            if current_month == "02":
                current_day = "28"
            elif current_month == "09" or current_month == "04" or current_month == "06" or current_month == "11":
                current_day = "30"
            else:
                current_day = "31"
        elif current_day[0] == "0" or current_day == "10":
            current_day = f"0{str(int(current_day) - 1)}"
        else:
            current_day = str(int(current_day) - 1)
        past_date = f"{str(past_year)}-{str(current_month)}-{str(current_day)}" 

    #we grab the index of the valid date 52 weeks ago and access the max within that
    index = date.index(past_date) #https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/

    recent_high = max(high[0:index])
    recent_low = min(low[0:index])


    #for date, prices in tsd.items():
    #    print(date)

    #https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/modules/csv.md
    #writes data into csv file
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{TICKER.lower()}_prices.csv")

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # writes header

        #https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s
        for d in date:
            daily_data = tsd[d]
            writer.writerow({"timestamp": d,
            "open": daily_data["1. open"],
            "high": daily_data["2. high"],
            "low": daily_data["3. low"], 
            "close": daily_data["4. close"],
            "volume": daily_data["5. volume"]})



    print("-------------------------")
    next_output = input("Press enter to see my stock recommendation.")
    print("-------------------------")
    print(f"SELECTED SYMBOL: {TICKER.upper()}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: {refreshed}")
    print("-------------------------")
    print(f"LATEST DAY: {latest_date}")
    print(f"LATEST CLOSE: {to_usd(float(recent_close))}")
    print(f"52-Week HIGH: {to_usd(float(recent_high))}")
    print(f"52-Week LOW: {to_usd(float(recent_low))}")
    print("-------------------------")

    #formulate recommendation

    yr_average = sum(open_p[0:index])/(index + 1)
    half_index = int(index/2)
    half_yr_average = sum(open_p[0:half_index])/(half_index + 1)
    high_threshold = min((1.5 * yr_average), (1.5 * half_yr_average))

    decision = ""
    reason = ""
    if close[0] > high_threshold:
        decision = "Sell"
        reason = "The stock seems to be overvalued. It's price is much higher than recent averages."
    elif half_yr_average > yr_average:
        if close[0] > half_yr_average:
            decision = "Buy"
            reason = "This stock is steadily trending upwards."
        else: #close[0] =< half_yr_average
            decision = "Sell"
            reason = "After recent, relative success, this stock seems to be falling in value."
    else: #yr_average >= half_yr_average
        if close[0] > half_yr_average:
            decision = "Buy"
            reason = "This stock seems to be rebounding from below average performance recently."
        else: #close[0] =< half_yr_average:
            decision = "Sell"
            reason = "This stock seems to be struggling in performance as of late."

    print(f"RECOMMENDATION: {decision}")
    print(f"RECOMMENDATION REASON: {reason}")
    print("-------------------------")
    print(f"Writing to a CSV file: {csv_file_path} ... ")
    print("-------------------------")

    # adapted from: https://plot.ly/python/getting-started/#initialization-for-offline-plotting
    plotly.offline.plot({
    "data": [go.Scatter(x= date, y= close)],
    "layout": go.Layout(title=f"Stock Price over Time: {TICKER.upper()}")
    }, auto_open=True)

    print("HAPPY INVESTING!")
    print("-------------------------")

