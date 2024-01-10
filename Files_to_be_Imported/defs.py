# Taken from bluefeversoft
API_KEY = "82327cb1b2120c2d6dce7f9f3c2ba5aa-831f9214a592b4e7ed8f1533d17f7b07"
OANDA_URL = 'https://api-fxpractice.oanda.com/v3'

SECURE_HEADER = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

HOLIDAYS = ['01/01', '15/01', '29/03', '31/03', '01/05', '04/07', '25/12']

ORDERCANCELLATION = 'orderCancelTransaction'
ACCOUNT_ID = '101-002-27805857-001'