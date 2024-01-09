import requests
import json

#Url con el Id_User para crear la SUCURSAL(1588285685)
url = 'https://api.mercadopago.com/users/1588285685/stores'

#Los headers que necesita la APIs para dar una respuesta
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685', #Modificar los AUTh de identificación de cada cuenta(APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685).
}

#Los datos a cargar de la Sucursal
SUCload = {
    'business_hours': {
        'monday': [
            {
                'open': '08:00',
                'close': '12:00',
            },
        ],
        'tuesday': [
            {
                'open': '13:00',
                'close': '21:00',
            },
        ],
    },
    'external_id': 'SUC002', #Asignar el id como se identificara a la sucursal para mas adelante
    'location': {
        'street_number': '1200',
        'street_name': 'Piedras',
        'city_name': 'Resistencia',
        'state_name': 'Chaco',
        'latitude': -27.467046189746227,
        'longitude': -58.98209356917159,
        'reference': 'Carniceria',
    },
    'name': 'La Candil',
}

response = requests.post(url, headers=headers, data=json.dumps(SUCload))
print(response.status_code)