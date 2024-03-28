import requests
import base64

class GetnetAPI:
    
    def make_request(self, endpoint):
        base_url = "https://api-sandbox.getnet.com.br/"
        full_url = base_url + endpoint
        return full_url
    
    
    def get_access_token(self, client_id, client_secret):
        endpoint = "auth/oauth/v2/token"
        token_url = self.make_request(endpoint)
        
        form_data = {
            'scope': 'oob',
            'grant_type': 'client_credentials'
        }
        
        auth_string = f"{client_id}:{client_secret}"
        auth_string_base64 = base64.b64encode(auth_string.encode()).decode()
        authorization_header = f"Basic {auth_string_base64}"
                
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': authorization_header
        }
        
        try:
            response = requests.post(token_url, data=form_data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            access_token = token_data.get('access_token')
            return access_token
        except requests.exceptions.HTTPError as err:
            
            print("-"*60)
            print(f"HTTP error occurred: {err}")

            return None
    
    
    def tokenize_card(self, access_token, card_number, customer_id=None, seller_id=None):
        endpoint = "v1/tokens/card"
        tokenization_url = self.make_request(endpoint)
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {access_token}'
        }
        
        data = {
            'card_number': card_number
        }
        
        if customer_id:
            data['customer_id'] = customer_id
        
        if seller_id:
            headers['Authorization'] += f', {seller_id}'
        
        try:
            response = requests.post(tokenization_url, json=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            token = token_data.get('number_token')
            return token
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return None
    
    
    def tokenize_brand(self, access_token, customer_id, card_pan, card_pan_source, card_brand, expiration_year, expiration_month, security_code, email):
        endpoint = "v1/tokenization/token"
        tokenization_url = self.make_request(endpoint)
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {access_token}'
        }
        
        data = {
            'customer_id': customer_id,
            'card': {
                'card_pan': card_pan,
                'card_pan_source': card_pan_source,
                'card_brand':card_brand,
                'expiration_year':expiration_year,
                'expiration_month':expiration_month,
                'security_code':security_code,
                'email':email,
            }
        }
        
        try:
            response = requests.post(tokenization_url, json=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            token = token_data.get('number_token')
            return token
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return None
    
    
    def make_credit_card_payment(self, access_token, payment_params):
        endpoint = "v1/payments/credit"
        payment_url = self.make_request(endpoint)
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {access_token}'
        }
                
        shipping_data = payment_params['shippings'][0]

        data = {
            'seller_id': payment_params['seller_id'],
            'amount': payment_params['amount'],
            'currency': payment_params['currency'],
            'order': payment_params['order'],
            'customer': payment_params['customer'],
            'device': payment_params['device'],
            'shippings': [shipping_data], 
            'shipping_amount': shipping_data['shipping_amount'],  
            'sub_merchant': payment_params['sub_merchant'],
            'credit': payment_params['credit'],
            'tokenization': payment_params['tokenization'],
            # 'wallet': payment_params['wallet']
        }

        try:
            response = requests.post(payment_url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            print("Response body:", response.text)
            return None
            
# ----------------------------------------------------------------------------------------
# Teste - Token de acesso 
# ----------------------------------------------------------------------------------------

api = GetnetAPI()

client_id = '926e3b0b-6219-4f26-8325-a04703fc558d'
client_secret = '1724725c-52ec-4254-a77e-f0ea11786d47'

access_token = api.get_access_token(client_id, client_secret)

print("-"*60)
print(f'Token acesso: {access_token}')
print("-"*60)

# ----------------------------------------------------------------------------------------
# Teste - Token do Cartão 
# ----------------------------------------------------------------------------------------


card_number = "5155901222280001"
customer_id = "customer_21081826"

card_token = api.tokenize_card(access_token, card_number, customer_id)

# if card_token:
#     print("-"*60)
#     print(f'Token do cartão gerado com sucesso: {card_token}')
#     print("-"*60)
# else:
#     print("-"*60)
#     print('Falha ao gerar o token do cartão.')
#     print("-"*60)
    
# ----------------------------------------------------------------------------------------
# Teste - Tokerização da Bandeira
# ------------ ----------------------------------------------------------------------------


"""
    PAN - Primary Account Number
    
    card_pan_source - Ele especifica como os dados do número do cartão foram obtidos ou fornecidos.
        Normalmente, os valores possíveis são: ON_FILE (Indica que o solicitante do token já possui os dados PAN em seus registros),
        MANUALLY_ENTERED (Indica que os dados do PAN foram digitados manualmente pelo titular do cartão.MANUALLY_ENTERED: Indica que
        os dados do PAN foram digitados manualmente pelo titular do cartão) e VIA_APPLICATION (Indica que os dados PAN (ou referência)
        foram fornecidos por um aplicativo emissor de cartões).
        
    card_brand - É o parâmetro que indica a bandeira do cartão de crédito ou débito. Em outras palavras, é o identificador da rede de 
        pagamento que emitiu o cartão. Alguns exemplos de bandeiras de cartão incluem Visa, Mastercard, American Express, Discover, 
        entre outras.
    
"""
        
        
card_pan = card_number
card_pan_source = 'MANUALLY_ENTERED'  
card_brand = 'VISA'  
expiration_year = '2025'
expiration_month = '12'
security_code = '436'
email = 'professional@email.com'

# if card_brand.upper() not in ['MASTERCARD', 'VISA']:
#     print("Apenas cartões Visa ou Mastercard podem ser tokenizados.")
# else:
#     token = api.tokenize_brand(access_token,
#                                customer_id,
#                                card_pan,
#                                card_pan_source,
#                                card_brand,
#                                expiration_year,
#                                expiration_month,
#                                security_code,
#                                email
#                                )
#     if token:
#         print("-"*60)
#         print(f'Token da bandeira gerado com sucesso: {token}')
#         print("-"*60)
#     else:
#         print("-"*60)
#         print('Falha ao gerar o token da bandeira.')
#         print("-"*60)

    
# ----------------------------------------------------------------------------------------
# Teste - Pgto Credito
# ------------ ----------------------------------------------------------------------------



payment_params = {
  "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
  "amount": 100,
  "currency": "BRL",
  "order": {
    "order_id": "6d2e4380-d8a3-4ccb-9138-c289182818a3"
  },
  "customer": {
    "customer_id": customer_id,
    "email": "customer@email.com.br",
    "document_type": "CPF",
    "document_number": "12345678912",
    "phone_number": "5551999887766",
    "billing_address": {
      "street": "Av. Brasil",
      "number": "1000",
      "city": "Porto Alegre",
      "state": "RS",
      "country": "Brasil",
      "postal_code": "90230060"
    }
  },
  "device": {
    "ip_address": "127.0.0.1",
    "device_id": "hash-device-id"
  },
  "shippings": [
    {
      "shipping_amount": 3000,
      "address": {
        "street": "Av. Brasil",
        "number": "1000",
        "city": "Porto Alegre",
        "state": "RS",
        "country": "Brasil",
        "postal_code": "90230060"
      }
    }
  ],
  "sub_merchant": {
    "identification_code": "9058344",
    "document_type": "CNPJ",
    "document_number": "20551625000159",
    "city": "Cidade",
    "state": "RS",
    "postal_code": "90520000"
  },
  "credit": {
    "delayed": False,
    "transaction_type": "FULL",
    "number_installments": 1,
    "card": {
      "number_token": card_token,
      "security_code": "123",
      "brand": "Mastercard",
      "expiration_month": "12",
      "expiration_year": "28"
    }
  },
  "tokenization": {
    "type": "ELO"
  }
}

result = api.make_credit_card_payment(access_token, payment_params)

if result:
    print("Payment successful!")
    print("Payment details:", result)
else:
    print("Payment failed!")