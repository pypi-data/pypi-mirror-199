from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

BATCH_SIZE = 1000

class UserRepoExtractor(ExtractorBase):
    def __init__(self, base_url: str, auth: Auth, dest: DataSink, evt: dict):
        super().__init__('github', '', 'user_repos', base_url, auth, dest)
        self.event = evt
        self.owner = evt['owner']
        self.urls = evt['repoUrls']

        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

    def extract(self):
        # print('To retrieve user repos')
        repos = []

        for url in self.urls:
            self.extract_repos(url, repos)

            if len(repos) >= BATCH_SIZE:
                self.dest.sink(repos)

                repos = []

        if len(repos):
            self.dest.sink(repos)

        # print(f'Finished loading user repos')
        

    def extract_repos(self, url, repos):
        if not url:
            return

        params = {
            'per_page': 100
        }

        page = 1
        
        while True:
            params['page'] = page

            resp = httpx.get(url, headers = self.headers, params = params)

            status = resp.status_code

            if status == 422:
                # print(f'HTTP status 422(Unprocessable Entity) received. this is not an error')
                break

            if status == 403:
                remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))
                
                if remain <= 0:
                    raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
                else:
                    raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

            if status != 200:
                raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

            if resp.text == '[]':
                break

            repos.extend(json.loads(resp.text))
            # self.user_repos = [*repos, *json.loads(resp.text)]
            page += 1