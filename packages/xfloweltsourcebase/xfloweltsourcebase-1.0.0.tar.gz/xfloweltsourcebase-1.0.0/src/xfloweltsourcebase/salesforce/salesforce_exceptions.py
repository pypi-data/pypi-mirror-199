class AuthorzationFailureException(Exception):
    def __init__(self, message: str):
        super().__init__(f'Invalid or expired auth token. Error message: {message}')
        self.status = 401
        