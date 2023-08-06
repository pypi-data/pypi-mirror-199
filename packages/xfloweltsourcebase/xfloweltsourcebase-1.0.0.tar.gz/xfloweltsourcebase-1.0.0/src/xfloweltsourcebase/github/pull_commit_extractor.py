from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 30
BATCH_SIZE = 300

class PullCommitExtractor(ExtractorBase):
    def __init__(self, base_url: str, auth: Auth, dest: DataSink, evt: dict):
        super().__init__('github', '', 'pull_commits', base_url, auth, dest)
        self.event = evt
        self.owner = evt['owner']
        self.urls = evt['commits']
        self.repo = evt['repo']
        # self.number = evt['number']

        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        self.commits = []

        # statistics
        self.num_extracted = 0

    def __extract_and_sink(self, url):
        params = {
            'per_page': PAGE_SIZE
        }

        eindex = url.index('/commits')
        sindex = url.index('/pulls') + 7
        number = int(url[sindex:eindex])

        # print(f'To extract pull commits at {url}, pull number: {number}')

        page = 1

        while True:
            params['page'] = page

            # print(f'To retrieve pull commits {url}. Query params: {params}')

            resp = httpx.get(url, headers = self.headers, params = params)
            self.num_calls += 1

            status = resp.status_code

            # foe below 2 status, they are not errors, let's just break out
            if status == 304 or status == 422:
                break

            if status == 403:
                remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))

                if remain <= 0:
                    raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
                else:
                    raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

            if status != 200:
                # print(f'WARNING: Got HTTP status {status} with GET at {url}')
                break

            self.num_success += 1

            if resp.text == '[]':
                # print(f'WARNING: Received empty response from GET at {url}')
                break

            commits = json.loads(resp.text)

            num = len(commits)

            self.num_extracted += num

            # print(f'pull commits retrieved. # of commits: {num}')

            for commit in commits:
                commit['pull_number'] = number
                self.commits.append(commit)

            if num < PAGE_SIZE:
                break

            page += 1


    def extract(self):
        # print(f'To retrieve pull commits for repo {self.repo}')

        for url in self.urls:
            self.__extract_and_sink(url)

        if len(self.commits):
            self.dest.sink(self.commits)

        if self.num_extracted <= 0:
            # print(f'WARNING: No commits extracted for pulls {self.urls}')
            pass
        

