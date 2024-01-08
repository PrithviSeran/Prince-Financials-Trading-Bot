# Prince-Financials-Trading-Bot

Prince Financials' Trading Bot is an open-source Forex trading bot that uses multiple indicators to make trades.

Prince Trading Bot utilizes Oanda's trading API to place trades (currently it uses the practice simulation API, so real money is not used) and runs on the Google Cloud Platform.

## How The Project Operates
For any of the currency pairs' time spread (per-minute values, per-hour values, daily values), the indicator values are calculated (for now it is **Relative Strength Index, Stochastic Oscilator, Aroon, and ADX**). If half or more indicators say Buy for a specfic currency pair, then a trade is placed through the OANDA API. If there is already a trade placed for currency pair and half or more imdactors say Sell, then that trade is sold. 
This entire program is deployed to Google Cloud, where it is run for every increment of the specified time-spread (If the indicators are based on hourly data, then the program is run hourly on the google cloud).

## Break Down of the Project
- ## Files_to_be_Imported
  - ### Defs.py
    - **API_KEY**: Contains the api key to make trades in OANDA's trading platform (**To make Trades through this project, you need add your own API key**)
    - **OANDA_URL**: The URL to which to send any type of API request
    - **SECURE_HEADER**: This is a Dictionary, which contains the API_KEY to make the request, and Content-Type specifies how we want the information to be formated.
    - **HOLIDAYS**: A list containing all the dates when then forex market is closed
   
  - ### all_apis.py
    - **Oanda_API Class**: Python object to interact with OANDA's API.
      - **make_request method**: Makes a HTTP request to OANDA's API
      - **place_trade method**: Places a trade with the specified amount of units in OANDA's trading platform
      - **close_trade method**: Closes a trade with the specfied trade id
      - **fetch_candlesticks**: Retrieves the candlestick data for the specified currency exchange from OANDA's API 

  - ### main.py
    - **data_information Class**: Python object to interact with the currency pair retirved from **Oanda_API.fetch_candlesticks**
      - **change_dataset**: Changes the dataset used for analysis.
      - **create_graph**: Creates a line graph using the dataset.
      - **add_indicator**: Adds a vertical dashed line indicator to the graph.
      - **adx**: Calculates the Average Directional Index (ADX).
      - **aroon**: Calculates the Aroon indicators.
      - **relative_strength_index**: Calculates the Relative Strength Index (RSI).
      - **stochastic_oscillator**: Calculates the Stochastic Oscillator values.
      - **make_analysis_dataframe**: Creates a DataFrame with various technical analysis indicators.
  
    - **indicators Class**: Python object to get trade signals
      - **enter_new_data**: Enters new data for various technical indicators.
      - **RSI_signal**: Generates a signal based on the Relative Strength Index (RSI).
      - **aroon_signal**: Generates a signal based on the Aroon Indicator.
      - **average_directional_index_signal**: Generates a signal based on the Average Directional Index.
      - **stochastic_oscillator_indicator_signal**: Generates a signal based on the Stochastic Oscillator.
      - **get_trade_action**: Determines the trade action based on accumulated signals.

    - **main function**: Based on the technical indicators calculated from the object above, a Forex trade is placed, sold, or nothing happens. Trades are placed through the Oanda_API object. Main function only runs once when called.
- ## Terras
  - ### Contains all the required Terraform files to create a google cloud storage bucket
- ## google_defs.py
  - **CLIENT_FILE**: relative path to your JSON authentication file
  - **SCOPES**: The scope URL for accssing Google Cloud APIS (use "https://www.googleapis.com/auth/cloud-platform" is you are unsure on what link to use)
- ## google_main.py
  - **Google_API Class**: Python object for interacting with various Google Cloud APIs.
    - **create_credentials**: Creates and retrieves Google API credentials.
    - **create_API_reaquest**: Creates an API request for a specific Google API.
    - **create_pubsub**: Creates a Pub/Sub topic using the Google Pub/Sub API.
    - **create_scheduler**: Creates a Cloud Scheduler job using the Google Cloud Scheduler API.
    - **pause_scheduler**: Pauses a Cloud Scheduler job using the Google Cloud Scheduler API.
    - **create_function**: Creates a Cloud Function using the Google Cloud Functions API.
    - **create_storage_object**: Creates a storage object using Terraform configurations.
  - **make_defs_to_import**: Adds the user's Oanda Account ID to the defs.py file in Files_to_be_Imported folder
  - **make_zip_store**: zips the Files_to_be_Imported folder
  - **main function**
    - **Bucket, Topic, and Job ID Setup:** The name for the google services are created based on the username. 
    - **Definitions File and Oanda Account ID:** The the Oanda account id is added to the defs.py file, and Files_to_be_Imported folder is zipped
    - **Google_API Object Initialization:**
    - **Credentials and Pub/Sub Topic Creation:** The credentials to use Google Cloud API's services is created, and a pubsub topic is created
    - **Cloud Scheduler Job Creation:** A cloud scheduler job is created to run on a certain increment (per minute, per hour, per day. This project uses hourly). This job is used to run the code in Files_to_be_Imported every time increment. 
    - **Storage Object Creation Using Terraform:** A storage bucket is created on the google cloud to store the zipped folder. The zipped folder is simultaneously uploaded to the bucket. 
    - **Cloud Function Creation:** Finaly, a google cloud function is created to run the script in the bucket. In this project, the script is run every hour, since the technicals are calculated on the hourly values. So every hour, based on the techincals, the code in the bucket is run, and the code either places a trade, sells an existing trade, or remain as it is. 
