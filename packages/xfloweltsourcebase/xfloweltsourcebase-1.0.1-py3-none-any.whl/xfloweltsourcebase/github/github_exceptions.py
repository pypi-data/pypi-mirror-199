class RateLimitReachedException(Exception):
    def __init__(self, retry_at: int):
        super().__init__(f'Github API rate limit reached. Retry at {retry_at}')
        self.retry_at = retry_at