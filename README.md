# Prince-Financials-Trading-Bot

Prince Financials' Trading Bot is an open-source Forex trading bot that uses multiple indicators to make trades.

Prince Trading Bot utilizes Oanda's trading API to place trades (currently it uses the practice simulation API, so real money is not used) and runs on the Google Cloud Platform.

## How The Project Operates
For any of the currency pairs' time spread (per-minute values, per-hour values, daily values), the indicator values are calculated (for now it is **Relative Strength Index, Stochastic Oscilator, Aroon, and ADX**). If half or more indicators say Buy for a specfic currency pair, then a trade is placed through the OANDA API. If there is already a trade placed for currency pair and half or more imdactors say Sell, then that trade is sold. 
This entire program is deployed to Google Cloud, where it is run for every increment of the specified time-spread (If the indicators are based on hourly data, then the program is run hourly on the google cloud).

## Break Down of the Project
