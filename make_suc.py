import requests
import json

url = 'https://api.mercadopago.com/users/1588285685/stores'

headers = {
    # Already added when you pass json= but not when you pass data=
    'Content-Type': 'application/json',
    'Authorization': 'Bearer APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685',
}

payload = {
    'business_hours': {
        'monday': [
            {
                'open': '08:00',
                'close': '12:00',
            },
        ],
        'tuesday': [
            {
                'open': '09:00',
                'close': '18:00',
            },
        ],
    },
    'external_id': 'SUC001',
    'location': {
        'street_number': '1200',
        'street_name': 'Piedras',
        'city_name': 'Resistencia',
        'state_name': 'Chaco',
        'latitude': -27.467046189746227,
        'longitude': -58.98209356917159,
        'reference': 'Carniceria',
    },
    'name': 'CARNEMISARIA',
}

response = requests.post(url, headers=headers, json=payload)
print(response.content)

if response.status_code == 200:
    print(response.status_code)
else:
    print(response.status_code)