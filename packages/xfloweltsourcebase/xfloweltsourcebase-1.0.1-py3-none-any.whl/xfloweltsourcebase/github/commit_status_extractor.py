from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 30

class CommitStatusExtractor(ExtractorBase):
    def __init__(self, base_url: str, auth: Auth, dest: DataSink, evt: dict):
        super().__init__('github', '', 'commit_statuses', base_url, auth, dest)
        self.event = evt
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.urls = evt['commits']
        self.repo = evt['repo']

        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        self.statuses = []

        self.num_extracted = 0

    def __extract_and_sink(self, url): 
        resp = httpx.get(f'{url}/status', headers = self.headers)
        self.num_calls += 1

        status = resp.status_code

        # foe below 2 status, they are not errors, let's just break out
        if status == 304 or status == 422:
            return

        if status == 403:
            remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))

            if remain <= 0:
                raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
            else:
                raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

        if status != 200:
            # print(f'WARNING: Got HTTP status {status} with GET at {url}')
            return

        self.num_success += 1

        if resp.text == '[]':
            # print(f'WARNING: Received empty response from GET at {url}')
            return

        sts = json.loads(resp.text)

        self.num_extracted += 1

        self.statuses.append(sts)

    def extract(self):
        # print(f'To retrieve commit statuses for repo {self.repo}')

        for url in self.urls:
            self.__extract_and_sink(url)

        if len(self.statuses):
            self.dest.sink(self.statuses)

        if not self.num_extracted:
            # print(f'WARNING: No statuses extracted for commits {self.urls}')
            pass