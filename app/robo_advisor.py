# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

print("REQUESTING SOME DATA FROM THE INTERNET...")

TICKER = "TSLA"
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
breakpoint()

tsd = parsed_response["Time Series (Daily)"]

for date, prices in tsd.items():
    print(date)



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")