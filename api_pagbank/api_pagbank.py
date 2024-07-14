

import requests
import os


def public_key():
    url = os.environ.get('URL_PAGBANK') +"/public-keys"
    payload = { "type": "card" }
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return(response.text)


def create_application():
    url = os.environ.get('URL_PAGBANK') + "/oauth2/application"
    
    print(url)

    payload = {
        "name": "DecorBook",
        "description": "Descrição da platforma",
        "site": "http://www.decorbook.com.br",
        "redirect_uri": "http://www.decorbook.com.br/callback",
    }
    
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {os.environ.get('TOKEN_PAGBANK')}",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)