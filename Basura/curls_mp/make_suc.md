curl -X POST \
      'https://api.mercadopago.com/users/1591852336/stores'\
       -H 'Content-Type: application/json' \
       -H 'Authorization: Bearer APP_USR-7911867245071721-121309-4863023be10971bc4f895f01d65866c6-1591852336' \
       -d '{
  "business_hours": {
    "monday": [
      {
        "open": "7:00",
        "close": "12:00"
      }
    ],
    "tuesday": [
      {
        "open": "13:00",
        "close": "20:00"
      }
    ]
  },
  "external_id": "SUC001",
  "location": {
    "street_number": "1200",
    "street_name": "Piedras",
    "city_name": "Resistencia",
    "state_name": "Chaco",
    "latitude": -27.467058208175082,
    "longitude": -58.98206851672713,
    "reference": "Supermercado"
  },
  "name": "Arcoiris2"
}'