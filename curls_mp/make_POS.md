curl -X POST \
      'https://api.mercadopago.com/pos'\
       -H 'Content-Type: application/json' \
       -H 'Authorization: Bearer APP_USR-7911867245071721-121309-4863023be10971bc4f895f01d65866c6-1591852336' \
       -d '{
  "category": 621102,
  "external_id": "SUC001POS001",
  "external_store_id": "SUC001",
  "fixed_amount": true,
  "name": "Ca_0101"
}