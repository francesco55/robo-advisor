# robo-advisor

## Overview

This application reads in historical stock price data, writes the data to a CSV file, gives a buy/sell recommendation, and outputs a graph of historical stock prices. It may also alert the user via text message if the given stock changes in price significantly (more than 4%).

## Installation

To install all necessary documents: fork this repository, clone your fork and download it onto your computer. Navigate to the files from the command-line with the given code.

```sh
cd ~/Documents/GitHub/shopping-cart
```

## Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```

Additionally, a .env file is essential to the security of your information in running this program. Create a .env file by command-line or in your text editor. We will put environment variables in this file.

## API Setup 

Your program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co). Go to the linked website and get a free API key. The program's source code should absolutely not include the secret API Key value, so we will use the .env file. Set an environment variable called `ALPHAVANTAGE_API_KEY`

```
ALPHAVANTAGE_API_KEY= "" #enter your API key here
```

## Twilio Setup

Twilio allows this application to send the user an SMS message given certain stock market conditions.

For SMS capabilities, [sign up for a Twilio account](https://www.twilio.com/try-twilio), click the link in a confirmation email to verify your account, then confirm a code sent to your phone to enable 2FA.

Then [create a new project](https://www.twilio.com/console/projects/create) with "Programmable SMS" capabilities. And from the console, view that project's Account SID and Auth Token. Update the contents of the ".env" file to specify these values as environment variables called `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`, respectively.

You'll also need to [obtain a Twilio phone number](https://www.twilio.com/console/sms/getting-started/build) to send the messages from. After doing so, update the contents of the ".env" file to specify this value (including the plus sign at the beginning) as an environment variable called `SENDER_SMS`.

Finally, set an environment variable called `RECIPIENT_SMS` to specify the recipient's phone number (including the plus sign at the beginning).

## Usage

The code should be ready to run!

Use the following code in terminal:

```sh
python robo_advisor.py
```


