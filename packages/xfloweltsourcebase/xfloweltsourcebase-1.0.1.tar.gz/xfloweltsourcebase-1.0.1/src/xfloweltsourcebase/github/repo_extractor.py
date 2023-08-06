from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.github.github_events import RepoTeamBroadcaster

import json
import httpx

PAGE_SIZE = 100
BATCH_SIZE = 50

class RepoExtractor(ExtractorBase):
    def __init__(self, owner: str, base_url: str, auth: Auth, dest: DataSink, broadcaster: RepoTeamBroadcaster):
        super().__init__('github', owner, 'repos', base_url, auth, dest)

        self.url = self.url_base + '/orgs' + '/' + owner + '/repos'

        self.broadcaster = broadcaster

        self.repos = []

    def extract(self):
        # print(f'To retrieve repositories for owner {self.owner}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': PAGE_SIZE
        }

        page = 1

        while True:
            params['page'] = page

            resp = httpx.get(self.url, headers = headers, params = params)

            status = resp.status_code

            # it is not an error, let's just break out. 422 = Unprocessable Entity
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

            batched = json.loads(resp.text)

            self.repos = [*self.repos, *batched]

            if len(batched) < PAGE_SIZE:
                break

            page += 1

        if len(self.repos):
            self.sink_and_broadcast()

    def sink_and_broadcast(self):
        print(f'# of repos: {len(self.repos)}')

        self.dest.sink(self.repos)

        evt = {
            'owner': self.owner,
            'data': []
        }

        for repo in self.repos:
            evt['data'].append({
                'repo': repo['id'],
                'repoName': repo['name'],
                'teams': repo['teams_url']
            })

            if len(evt['data']) >= BATCH_SIZE:
                self.broadcaster.broadcast(evt)

                evt['data'] = []
        
        if len(evt['data']):
                self.broadcaster.broadcast(evt)
