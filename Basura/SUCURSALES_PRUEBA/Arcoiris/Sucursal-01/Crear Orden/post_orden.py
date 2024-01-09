import requests
import json

url = 'https://api.mercadopago.com/mpmobile/instore/qr/1591852336/SUC001POS002'

headers = {
    'Content-Type': 'application/json',
    'X-Ttl-Store-Preference': "180" ,
    'Authorization': 'Bearer APP_USR-7911867245071721-121309-4863023be10971bc4f895f01d65866c6-1591852336'
}

payload = {
  "external_reference": "Factura-0001",
  "items": [
    {
      "id": 78123172,
      "title": "Arcoiris",
      "currency_id": "ARG",
      "unit_price": 2000,
      "quantity": 1,
      "description": "MERCADERIAS",
      "picture_url": "https://www.bubbleaventuras.com/wp-content/uploads/2020/06/arcoiris-casero.jpg"
    },
    {
      "id": 78123172,
      "title": "Arcoiris",
      "currency_id": "ARG",
      "unit_price": 1500,
      "quantity": 1,
      "description": "MERCADERIAS",
      "picture_url": "https://www.bubbleaventuras.com/wp-content/uploads/2020/06/arcoiris-casero.jpg"
    }
  ],
  "notification_url": "http://www.yourserver.com"
}


response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response)