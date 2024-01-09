import requests
import json

url = 'https://api.mercadopago.com/pos'

hedears = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer APP_USR-7911867245071721-121309-4863023be10971bc4f895f01d65866c6-1591852336'
}

POSload = {
    "category": 621102,
    "external_id": "SUC001POS002",
    "external_store_id": "SUC001",
    "fixed_amount": True,
    "name": "Ca_0102"
}

response = requests.post(url, headers=hedears, data=json.dumps(POSload))
print(response)