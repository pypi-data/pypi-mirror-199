class NotImplementedException(Exception):
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause

class UnknownHttpStatusException(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code

    def status_code(self):
        return self.status_code

class HttpStatus429Exception(Exception):
    def __init__(self):
        super().__init__('Too Many Requests')
        self.status_code = 429

    def status_code(self):
        return 429