import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import defs
import json
import os


# Taken from bluefeversoft
class Oanda_API:
    """
    Class for interacting with the OANDA API.
    """

    def __init__(self):
        """
        Initializes the OANDA API object with a session.
        """
        self.session = requests.Session()

    def make_request(self, url, params={}, added_headers=None, verb='get', data=None, code_ok=200):
        """
        Makes a request to the OANDA API.

        Parameters:
        - url (str): The API endpoint URL.
        - params (dict): Query parameters for the request.
        - added_headers (dict): Additional headers for the request.
        - verb (str): HTTP verb for the request ('get', 'post', 'put').
        - data: Request data, used for POST and PUT requests.
        - code_ok (int): Expected HTTP status code for a successful response.

        Returns:
        - tuple: A tuple containing the HTTP status code and the JSON response.
        """
        headers = defs.SECURE_HEADER

        if added_headers is not None:
            for k in added_headers.keys():
                headers[k] = added_headers[k]

        try:
            response = None
            if verb == 'post':
                response = self.session.post(url, params=params, headers=headers, data=data)
            elif verb == 'put':
                response = self.session.put(url, params=params, headers=headers, data=data)
            else:
                response = self.session.get(url, params=params, headers=headers, data=data)

            status_code = response.status_code

            if status_code == code_ok:
                json_response = response.json()
                return status_code, json_response
            else:
                return status_code, None

        except:
            print("ERROR")
            return 400, None

    def place_trade(self, units):
        """
        Places a trade using the OANDA API.

        Parameters:
        - units (int): Number of units for the trade.

        Returns:
        - tuple: A tuple containing the HTTP status code and the JSON response.
        """
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/orders"

        data = {
            "order": {
                "units": units,
                "instrument": "EUR_USD",
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }

        status_code, json_code = self.make_request(url, verb="post", data=json.dumps(data), code_ok=201)

        return status_code, json_code

    def close_trade(self, trade_id):
        """
        Closes a trade using the OANDA API.

        Parameters:
        - trade_id (int): The ID of the trade to close.

        Returns:
        - bool: True if the trade is closed successfully, False otherwise.
        """
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        status_code, json_data = self.make_request(url, verb='post', code_ok=200)

        if status_code != 200:
            return False

        return True

    def fetch_candlesticks(self, instrument, candles_count, granularity):
        """
        Fetches candlestick data for a given instrument.

        Parameters:
        - instrument (str): The trading instrument (e.g., 'EUR_USD').
        - candles_count (int): Number of candlesticks to fetch.
        - granularity (str): Granularity of the candlesticks (e.g., 'M1', 'H1').

        Returns:
        - pd.DataFrame: A pandas DataFrame containing candlestick data.
        """
        url = f"{defs.OANDA_URL}/instruments/{instrument}/candles?count={candles_count}&price=M&granularity={granularity}"

        candles = self.make_request(url)

        closeings = []
        highs = []
        lows = []
        openings = []

        for i in range(len(candles[1]['candles'])):
            closeings.append(float(candles[1]['candles'][i]['mid']['c']))
            openings.append(float(candles[1]['candles'][i]['mid']['o']))
            highs.append(float(candles[1]['candles'][i]['mid']['h']))
            lows.append(float(candles[1]['candles'][i]['mid']['l']))

        current_data = {"BC": closeings,
                        "BH": highs,
                        "BL": lows,
                        "BO": openings}

        current_dataframe = pd.DataFrame(current_data)

        return current_dataframe


def main():
    oanda = Oanda_API()

    candles = oanda.fetch_candlesticks('EUR_USD', '100', 'H1')

    print(candles)

if __name__ == "__main__":

   main()

