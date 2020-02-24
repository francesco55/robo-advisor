# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def to_usd(my_price):
    
    #Converts a numeric value to usd-formatted string, for printing and display purposes.
    #Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    #Param: my_price (int or float) like 4000.444444
    #Example: to_usd(4000.444444)
    #Returns: $4,000.44
    
    return f"${my_price:,.2f}"

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("REQUESTING SOME DATA FROM THE INTERNET...")

TICKER = input("Please enter the company's ticker.")
#ticker validation
ticker_max = 4
if type(TICKER) == str:
    if len(TICKER) > ticker_max:
        print("This is not a valid ticker")
        exit()
else:
    print("this is not a valid ticker")
    exit()

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={TICKER}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)

#input validation

if "Error Message" in response.text:
    print("There is an error with either your inputted ticker or api key.")
    print("Please look into both and try again")
    exit()


parsed_response = json.loads(response.text)
print(parsed_response)
refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

date = list(tsd.keys()) #https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
recent_close = tsd[str(date[0])]["4. close"]
latest_date = date[0]

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

recent_high = max(high)
recent_low = min(low)


#for date, prices in tsd.items():
#    print(date)



print("-------------------------")
print(f"SELECTED SYMBOL: {TICKER}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {refreshed}")
print("-------------------------")
print(f"LATEST DAY: {latest_date}")
print(f"LATEST CLOSE: {to_usd(float(recent_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")