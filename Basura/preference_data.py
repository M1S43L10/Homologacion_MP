import mercadopago

sdk = mercadopago.SDK("APP_USR-3774512295656164-121208-e45df91faddd6fd608de107d1db2971f-1588285685")

preference_data = {
    "items": [
        {
            "title": "Osobuco",
            "unit_price": 1000,
            "quantity": 1
        }
    ],
    "purpose": "wallet_purchase"
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]

print(preference)
