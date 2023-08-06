from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

class CommitDetailExtractor(ExtractorBase):
    def __init__(self, base_url: str, auth: Auth, dest: DataSink, evt: dict):
        super().__init__('github', '', 'commit_details', base_url, auth, dest)
        self.event = evt
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.urls = evt['commits']
        self.repo = evt['repo']

    def extract(self):
        # print(f'To retrieve commit details for repo {self.repo}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        commits = []

        for url in self.urls:
            resp = httpx.get(url, headers = headers)
            self.num_calls += 1

            status = resp.status_code

            # foe below 2 status, they are not errors, let's just break out
            if status == 304 or status == 422:
                continue

            if status == 403:
                remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))
                if remain <= 0:
                    raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
                else:
                    raise UnknownHttpStatusException(status, f'Github response: {resp.text}')


            if status != 200:
                # print(f'WARNING: Got HTTP status {status} with GET at {url}')
                continue

            self.num_success += 1

            if resp.text == '[]':
                # print(f'WARNING: Received empty response from GET at {url}')
                continue

            commits.append(json.loads(resp.text))

        self.dest.sink(commits)