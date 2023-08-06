from xfloweltsourcebase.base.auth import BearerTokenAuth

import json
import httpx

class Authorizer(BearerTokenAuth):
    def __init__(self, client_id: str, client_secret: str, username: str, password: str):
        super().__init__(None)

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

        self.authorized = False
        self.error = None

        self.__authorize()

    def reauthorize(self):
        self.token = None
        self.authorized = False
        self.error = None

        self.__authorize()        

    def __authorize(self):
        if self.authorized:
            return
        
        form_data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }

        headers = {
            'Accept': 'application/json'
        }
        
        endpoint = 'https://login.salesforce.com/services/oauth2/token'

        resp = httpx.post(endpoint, headers = headers, data = form_data)

        if resp.status_code == 200:
            parsed = json.loads(resp.text)

            self.token = parsed['access_token']
            self.authorized = True
        else:
            self.error = resp.text

        

