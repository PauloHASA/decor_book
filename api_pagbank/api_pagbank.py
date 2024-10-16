import requests
import os
import json

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


def checkouts_method(name, email, tax_id, phone_country, phone_area, phone_number, reference_id, item_name, quantity, unit_amount):
    """
    Cria um checkout utilizando o PagSeguro.

    Parameters:
        name (str): Nome do cliente.
        email (str): Email do cliente.
        tax_id (str): CPF ou CNPJ do cliente.
        phone_country (str): Código do país do telefone.
        phone_area (str): DDD do telefone.
        phone_number (str): Número do telefone.
        reference_id (str): Referência do produto.
        item_name (str): Nome do produto.
        quantity (int): Quantidade do produto.
        unit_amount (int): Valor unitário do produto em centavos.

    Returns:
        dict: Resposta da API com os detalhes do checkout.
        
    """
    url = "https://sandbox.api.pagseguro.com/checkouts"
    
    
    payload = {
        "customer": {
            "phone": {
                "country": phone_country,
                "area": phone_area,
                "number": phone_number
            },
            "name": name,
            "email": email,
            "tax_id": tax_id
        },
           "shipping": {
            "type": "FREE",
            "amount": 0,
            "service_type": "PAC",
            "address_modifiable": True
        },
        "reference_id": reference_id,
        "customer_modifiable": True,
        "items": [
            {
                "reference_id": reference_id,
                "name": item_name,
                "quantity": quantity,
                "unit_amount": unit_amount,
            }
        ],
        "additional_amount": 0,
        "discount_amount": 0,
        "payment_methods": [{
                "type": "credit_card",
                "brands": ["mastercard"]
            }, {
                "type": "credit_card",
                "brands": ["visa"]
            }, {
                "type": "debit_card",
                "brands": ["visa"]
            }, { "type": "PIX" }, { "type": "BOLETO" }],
            "soft_descriptor": "xxxx",
            "redirect_url": "https://decorbook.com.br/paid",
            "return_url": "https://decorbook.com.br/paid"
        }
    
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "Content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


