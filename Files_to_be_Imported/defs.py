# Taken from bluefeversoft
API_KEY = "YOUR OANDA API KEY"
OANDA_URL = 'https://api-fxpractice.oanda.com/v3'

SECURE_HEADER = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

HOLIDAYS = ['01/01', '15/01', '29/03', '31/03', '01/05', '04/07', '25/12']

ORDERCANCELLATION = 'orderCancelTransaction'
ACCOUNT_ID = 'YOUR OANDA ACCOUNT ID'
