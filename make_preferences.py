
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("APP_USR-2060722498903714-121207-68deb75604fc126309c760e053429c75-216258049")


preference_data = {
    "items": [
        {
            "title": "Osobuco",
            "unit_price": 1050,
            "quantity": 1
        }
    ],
    "purpose": "wallet_purchase"
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]
