import mercadopago
from flask import Flask, request

app = Flask(__name__)

sdk = mercadopago.SDK("APP_USR-2145212492623165-011911-5c43c65057abe353c7180187b1ac5867-99549809")


def getToken(card_number, security_code, expiration_month, expiration_year, name, cpf):
    card_token_object = {
        "card_number": card_number,
        "security_code": security_code,
        "expiration_month": expiration_month,
        "expiration_year": expiration_year,
        "cardholder": {
            "name": name,
            "identification": {
                "CPF": cpf
            }
        }
    }

    card_token_created = sdk.card_token().create(card_token_object)

    if 'id' in card_token_created['response']:
        return card_token_created['response']['id']

    return None


def paymentSend(amount, token, payment_method_id, installments, email):
    payment_data = {
        "transaction_amount": amount,
        "token": token,
        "payment_method_id": payment_method_id,
        "installments": installments,
        "description": "Assinatura do aplicativo Via.Jus",
        "payer": {
            "email": email,
        },
        "external_reference": "MP0001",
        "notification_url": "https://meuservidor.com/webhook",
        "statement_descriptor": "Assinatura Via.Jus",
        "additional_info": {
            "items": [{
                "id": 1,
                "category_id": "subscription",
                "title": "Assinatura",
                "description": "Assinatura para utilização de uma conta de advogado no aplicativo do Via.Jus",
                "type": "subscription",
                "quantity": 1,
                "unit_price": amount,
                "warranty": False,
            }]
        },
    }

    result = sdk.payment().create(payment_data)
    print(result)
    payment_request = result["response"]["id"]
    payment_found = sdk.payment().get(payment_request)

    print(payment_found)

    return payment_found


@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    generated_Token = getToken(data['card_number'], data['security_code'], data['expiration_month'],
                               data['expiration_year'], data['name'], data['cpf'])
    response = paymentSend(data['amount'], generated_Token, data['payment_method_id'], data['installments'],
                           data['email'])

    return response


app.run(port=8080, host='localhost', debug=True)
