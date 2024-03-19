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
        
        print("-"*60)
        print(authorization_header)
        
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

# Testes

api = GetnetAPI()

client_id = '926e3b0b-6219-4f26-8325-a04703fc558d'
client_secret = '1724725c-52ec-4254-a77e-f0ea11786d47'

access_token = api.get_access_token(client_id, client_secret)

if access_token:
    print("-"*60)
    print(f'Token de acesso obtido com sucesso: {access_token}')
    print("-"*60)
else:
    print("-"*60)
    print('Falha ao obter o token de acesso.')
    print("-"*60)

