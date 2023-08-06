from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_events import CommitEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

BATCH_SIZE = 10
PAGE_SIZE = 30

class CommitExtractor(ExtractorBase):
    def __init__(
        self, 
        fetch_at: str,
        owner: str, 
        repo: str, 
        base_url: str, 
        auth: Auth, 
        since: str,
        until: str,
        dest: DataSink, 
        broadcaster: CommitEventBroadcaster):
        super().__init__('github', owner, 'commits', base_url, auth, dest)

        self.repo = repo
        # self.url = self.url_base + '/repos' + '/' + owner + '.'/teams'
        self.url = f'{self.url_base}/repos/{owner}/{repo}/commits'
        self.broadcaster = broadcaster
        self.since = since
        self.until = until
        self.fetch_at = fetch_at
        self.commits = []

    def extract(self):
        # print(f'To retrieve commits from {self.url}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': PAGE_SIZE,
            'since': self.since,
            'until': self.until
        }

        page = 1

        while True:
            params['page'] = page

            resp = httpx.get(self.url, headers = headers, params = params)
            self.num_calls += 1

            status = resp.status_code

            # print(f'got https staus: {status}')

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
                raise UnknownHttpStatusException(status, f'Github response: {resp.text}')
            
            self.num_success += 1

            if resp.text == '[]':
                break

            batch = json.loads(resp.text)
            # print(f'batch: {batch}')

            self.commits = [*self.commits, *batch]

            # print(f'commits: {self.commits}')

            if len(batch) < PAGE_SIZE:
                break

            page += 1

        # print(f'now, len = {len(commits)}')

        if len(self.commits) > 0:
            self.sink_and_broadcast()
        
    def sink_and_broadcast(self):
        # print(f'# of commits: {len(self.commits)}. org: {self.owner}, repo: {self.repo}')
        self.dest.sink(self.commits)

        evt = {
            'owner': self.owner,
            'fetchedAt': self.fetch_at,
            'repo': self.repo,
            'commits': [],
            'comments': []
        }

        for commit in self.commits:
            evt['commits'].append(commit['url'])
            evt['comments'].append(commit['comments_url'])

            if len(evt['commits']) >= BATCH_SIZE:
                self.broadcaster.broadcast(evt)
                evt['commits'] = []
                evt['comments'] = []

        if len(evt['commits']):
            self.broadcaster.broadcast(evt)
            evt['commits'] = []
            evt['comments'] = []