# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from keyword import iskeyword
import plotly
import plotly.graph_objs as go
from twilio.rest import Client

load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"

#https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
def hasNumbers(inputString):
    """
    accepts a string as an argument and returns a bool variable that yields true if a string has numbers and false if a string does not
    """
    return any(char.isdigit() for char in inputString)

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

if __name__ == "__main__":
    print("This application gathers a company's recent stock data, stores the data in a CSV file, and outputs a recommendation for purchase.")
    print("You may enter at most 5 stock tickers per minute.")
    print("Enter the tickers one by one. Enter 'DONE' when you are finished entering tickers.")
    print("Thank you!")


    # adapted from shopping_cart.py
    # multiple tickers input and validation
    ticker_list = []
    ticker_max = 5

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
        print("URL:", request_url)
        print("REQUESTING SOME DATA FROM THE INTERNET...")

        response = requests.get(request_url)

        #input validation

        if "Error Message" in response.text:
            print("ERROR")
            print(f"There is an error with either your inputted ticker ({TICKER}) or api key.")
            print("Please look into both and try again")
            print("___________________________________")
            continue

        if "higher API call frequency" in response.text:
            print("   ERROR   ")
            print("The source for stock price data has given the following error message:")
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

        # the following code checks if there is market data for the date exactly one year ago
        # if there is no market data one year ago exactly, the day prior is checked until a valid date is found

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

        recent_high = high[0]
        recent_low = low[0]
        yr_high = max(high[0:index])
        yr_low = min(low[0:index])


        #for date, prices in tsd.items():
        #    print(date)

        print("-------------------------")
        print(f"SELECTED SYMBOL: {TICKER.upper()}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print(f"REQUEST AT: {refreshed}")
        print("-------------------------")
        print(f"LATEST DAY: {latest_date}")
        print(f"LATEST CLOSE: {to_usd(float(recent_close))}")
        print(f"LATEST HIGH: {to_usd(float(recent_high))}")
        print(f"LATEST LOW: {to_usd(float(recent_low))}")
        print("-------------------------")
        print(f"52-Week HIGH: {to_usd(float(yr_high))}")
        print(f"52-Week LOW: {to_usd(float(yr_low))}")
        print("-------------------------")
        next_output = input("Press enter to see my stock recommendation.")
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
        print(f"Recommendations were made by comparing the current stock price to 52 week ({to_usd(float(yr_average))}) and 26 week ({to_usd(float(half_yr_average))}) averages.")
        print("-------------------------")

        #https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/modules/csv.md
        #writes data into csv file
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{TICKER.lower()}_prices.csv")

        csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

        print(f"Writing to a CSV file: {csv_file_path} ... ")

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
        input("Press enter to see a graph of stock prices over time.")
        print("Graphing 52 week data ...")

        # adapted from: https://plot.ly/python/getting-started/#initialization-for-offline-plotting
        plotly.offline.plot({
        "data": [go.Scatter(x= date[0:index], y= close[0:index])],
        "layout": go.Layout(title=f"Stock Price over Time: {TICKER.upper()}")
        }, auto_open=True)

        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")

        # Send SMS if daily stock price change is greater than 4%

        TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
        TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
        SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
        RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

        # AUTHENTICATE

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # COMPILE REQUEST PARAMETERS (PREPARE THE MESSAGE) and ISSUE REQUEST (SEND SMS)
        percent_change = round((((close[0] - open_p[0])/open_p[0])*100), 2)
        if percent_change > 4:
            content = f"Hello, this is a message from your Investment RoboAdvisor. {TICKER.upper()} is up {percent_change}% since markets opened this morning!"
            message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
        elif percent_change < -4:
            percent_change = percent_change * (-1)
            content = f"Hello, this is a message from your Investment RoboAdvisor. {TICKER.upper()} is down {percent_change}% since markets opened this morning."
            message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)


