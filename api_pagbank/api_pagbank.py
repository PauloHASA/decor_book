import requests
import os
import json

from datetime import datetime, timedelta

def public_key():
    """
    Obtém a chave pública para pagamentos com cartão.

    Returns:
        dict: Resposta da API com a chave pública.
    """
    url = os.environ.get('URL_PAGBANK') + "/public-keys"
    payload = {"type": "card"}
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def create_application():
    """
    Cria uma nova aplicação para a plataforma PagBank.

    Returns:
        dict: Resposta da API com detalhes da aplicação criada.
    """
    url = os.environ.get('URL_PAGBANK') + "/oauth2/application"
    payload = {
        "name": "DecorBook",
        "description": "Descrição da plataforma",
        "site": "http://www.decorbook.com.br",
        "redirect_uri": "http://www.decorbook.com.br/callback",
    }
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def payment_pix(name, email, tax_id, phone, item_name, amount):
    """
    Cria um pagamento utilizando Pix.

    Returns:
        dict: Resposta da API com os detalhes do pagamento e QR code.
    
    """
    url = os.environ.get('URL_PAGBANK') + "/orders"
    payload = {
        "customer": {
            "name": name,
            "email": email,
            "tax_id": tax_id,
            "phones": [
                {
                    "country": "55",
                    "area": "11",
                    "number": phone,
                    "type": "MOBILE"
                }
            ]
        },
        "reference_id": "ex-00001",
        "items": [
            {
                "reference_id": "item-0001",
                "name": item_name,
                "quantity": 1,
                "unit_amount": amount
            }
        ],
        "qr_codes": [
            {
                "amount": {
                    "value": 500
                }
            }
        ],
        "notification_urls": ["https://meusite.com/notificacoes"]
    }
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def checkouts_method(request, plan_id):
    """
    Cria um checkout utilizando o PagSeguro.

    Parameters:
        plan_id: Tipo do plano.

    Returns:
        dict: Resposta da API com os detalhes do checkout.
        
    """
    expiration_date = (datetime.now() + timedelta(minutes=30)).strftime(
            "%Y-%m-%dT%H:%M:%S-03:00"
    )  # Coloquei aqui um tempo de expiração de 30 minutos

    if plan_id == "annual":
        reference_id = "Plano Anual"
        unit_amount = 129900
        max_installments = 12
    elif plan_id == "semester":
        reference_id = "Plano Semestral"
        unit_amount = 89900
        max_installments = 6
    else:
        return None

    url = "https://sandbox.api.pagseguro.com/checkouts"
    payload = {
        "reference_id": reference_id,
        "expiration_date": expiration_date,
        "customer": {
            "name": request.user.full_name,
            "email": request.user.email,
        },
        "items": [
            {
                "reference_id": reference_id,
                "name": f"{reference_id}",
                "quantity": 1,
                "unit_amount": unit_amount,
                "image_url": "https://www.example.com/product-image.jpg",
            }
        ],
        "payment_methods": [
            {
                "type": "credit_card",
                "brands": ["mastercard", "visa", "amex", "elo"],
            },
            {"type": "debit_card", "brands": ["mastercard", "visa", "amex", "elo"]},
            {"type": "BOLETO"},
            {"type": "PIX"},
        ],
        "payment_methods_configs": [
            {
                "type": "credit_card",
                "config_options": [
                    {
                        "option": "INSTALLMENTS_LIMIT",
                        "value": max_installments,
                    },
                    {
                        "option": "INTEREST_FREE_INSTALLMENTS",
                        "value": max_installments,
                    },
                ],
            }
        ],
        "soft_descriptor": "DECORBOOK",
            "redirect_url": "https://decorbook.com.br/portfolio/payment_success/",
            "return_url": "https://decorbook.com.br/portfolio/payment_success/",   
        }

    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "Content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    return response
