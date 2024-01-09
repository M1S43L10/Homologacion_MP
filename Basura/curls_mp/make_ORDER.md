curl -X POST \
      'https://api.mercadopago.com/mpmobile/instore/qr/1591852336/SUC001POS001'\
       -H 'Content-Type: application/json' \
       -H 'X-Ttl-Store-Preference: 180' \,
       -H 'Authorization: Bearer APP_USR-7911867245071721-121309-4863023be10971bc4f895f01d65866c6-1591852336' \
       https://api.mercadopago.com/V1/payments
       -d '{
  "external_reference": "Factura-0001",
  "items": [
    {
      "id": 78123172,
      "title": "Arcoiris",
      "currency_id": "ARG",
      "unit_price": 1200,
      "quantity": 1,
      "description": "MERCADERIAS",
      "picture_url": "https://www.bubbleaventuras.com/wp-content/uploads/2020/06/arcoiris-casero.jpg"
    },
    {
      "id": 78123172,
      "title": "Arcoiris",
      "currency_id": "ARG",
      "unit_price": 2530,
      "quantity": 1,
      "description": "MERCADERIAS",
      "picture_url": "https://www.bubbleaventuras.com/wp-content/uploads/2020/06/arcoiris-casero.jpg"
    }
  ],
  "notification_url": "http://www.yourserver.com"
}'