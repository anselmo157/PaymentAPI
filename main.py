import mercadopago
from flask import Flask, jsonify, request

app = Flask(__name__)

sdk = mercadopago.SDK("TEST-2145212492623165-011911-c743112a41ebb1f41c9dc48330effff8-99549809")


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

    return card_token_created['response']['id']


def paymentSend(amount, token, payment_method_id, installments, email):
    payment_data = {
        "transaction_amount": amount,
        "token": token,
        "description": "Assinatura do aplicativo ViaJus",
        "payment_method_id": payment_method_id,
        "installments": installments,
        "payer": {
            "email": email,
        }
    }
    result = sdk.payment().create(payment_data)
    payment_request = result["response"]["id"]
    payment_found = sdk.payment().get(payment_request)

    print(payment_found)
    for key in payment_found['response'].keys():
        if payment_found['response'][key] is not None:
            print(key + ' : ' + str(payment_found['response'][key]))


@app.route('/payment', methods=['POST'])
def payment():
    # generated_Token = getToken("4235647728025682", "123", "11", "2025", "Lucas Firmiano", "19119119100")
    # paymentSend(100, generated_Token, "visa", 5, "anselmoparente@gmail.com")
    data = request.get_json()
    print(data)
    return {
        'deu bom': True
    }


app.run(port=5000, host='localhost', debug=True)
