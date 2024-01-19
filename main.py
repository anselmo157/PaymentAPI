import mercadopago
from datetime import datetime

sdk = mercadopago.SDK("TEST-2145212492623165-011911-c743112a41ebb1f41c9dc48330effff8-99549809")

card_token_object = {
            "card_number": "4235647728025682",
            "security_code": "123",
            "expiration_year": "2025",
            "expiration_month": "11",
            "cardholder": {
                "name": "APRO",
                "identification": {
                    "CPF": "19119119100"
                }
            }
        }

card_token_created = sdk.card_token().create(card_token_object)

payment_data = {
    "transaction_amount": 100,
    "token": card_token_created["response"]["id"],
    "description": "Assinatura do aplicativo ViaJus",
    "payment_method_id": 'visa',
    "installments": 1,
    "payer": {
        "email": 'anselmoparente@gmail.com',
    }
}
result = sdk.payment().create(payment_data)
payment = result["response"]

payment_found = sdk.payment().get(payment["id"])

print(payment_found)
