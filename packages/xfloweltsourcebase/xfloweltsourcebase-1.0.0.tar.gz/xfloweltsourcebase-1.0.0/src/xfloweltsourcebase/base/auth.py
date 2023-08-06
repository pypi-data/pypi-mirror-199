class Auth:
    def __init__(self, type: str):
        self.type = type

class BearerTokenAuth(Auth):
    def __init__(self, token: str):
        super().__init__('Bearer')

        self.token = token

class BasicAuth(Auth):
    def __init__(self, username: str, password: str):
        super().__init__('Basic')

        self.username = username
        self.password = password