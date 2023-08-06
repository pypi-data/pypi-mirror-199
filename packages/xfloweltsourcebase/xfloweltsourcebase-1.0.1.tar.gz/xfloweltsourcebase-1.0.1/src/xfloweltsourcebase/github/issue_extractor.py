from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_events import IssueEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

COMMIT_BATCH_SIZE = 200
COMMIT_PAGE_SIZE = 30

class IssueExtractor(ExtractorBase):
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
        broadcaster: IssueEventBroadcaster, 
        page_size = COMMIT_PAGE_SIZE):
        super().__init__('github', owner, 'issues', base_url, auth, dest)

        self.repo = repo
        # self.url = self.url_base + '/repos' + '/' + owner + '.'/teams'
        self.url = f'{self.url_base}/repos/{owner}/{repo}/issues'
        self.page_size = page_size
        self.broadcaster = broadcaster
        self.since = since
        self.until = until
        self.fetch_at = fetch_at


    def extract(self):
        # print(f'To retrieve issues from {self.url}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': self.page_size,
            'since': self.since,
            'until': self.until,
            'sort': 'updated'
        }

        page = 1
        issues = []
        evt = {
            'owner': self.owner,
            'fetchedAt': self.fetch_at,
            'repo': self.repo,
            'events': [],
            'comments': []
        }

        while True:
            params['page'] = page

            resp = httpx.get(self.url, headers = headers, params = params)

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

            if resp.text == '[]':
                break

            batch = json.loads(resp.text)
            # print(f'batch: {batch}')

            for issue in batch:
                evt['events'].append(issue['events_url'])
                evt['comments'].append(issue['comments_url'])

            issues = [*issues, *batch]

            # print(f'issues: {issues}, evt: {evt}')

            if len(issues) >= COMMIT_BATCH_SIZE:
                self.sink_and_broadcast(issues, evt)

                issues = []
                evt['events'] = []
                evt['comments'] = []

            page += 1

        # print(f'now, len = {len(commits)}')

        if len(issues):
            self.sink_and_broadcast(issues, evt)
        
    def sink_and_broadcast(self, issues: list, evt: dict):
        # print(f'# of issues: {len(issues)}. org: {self.owner}, repo: {self.repo}')
        self.dest.sink(issues)

        self.broadcaster.broadcast(evt)