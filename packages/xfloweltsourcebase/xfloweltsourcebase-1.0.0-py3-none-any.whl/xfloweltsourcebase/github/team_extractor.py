from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.constants import DFT_PAGE_SIZE
from xfloweltsourcebase.github.github_events import TeamMemberEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

BATCH_SIZE = 50

class TeamExtractor(ExtractorBase):
    def __init__(self, owner: str, base_url: str, auth: Auth, dest: DataSink, broadcaster: TeamMemberEventBroadcaster, page_size = DFT_PAGE_SIZE):
        super().__init__('github', owner, 'teams', base_url, auth, dest)

        self.url = self.url_base + '/orgs' + '/' + owner + '/teams'
        self.page_size = page_size
        self.broadcaster = broadcaster

        self.teams = []

    def extract(self):
        # print(f'To retrieve teams for owner {self.owner}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': self.page_size
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

            self.teams = [*self.teams, *batched]

            if len(batched) < self.page_size:
                break

            page += 1

        if len(self.teams):
            self.sink_and_broadcast()


    def create_member_urls(self):
        member_urls = []

        for team in self.teams:
            member_url = team.get('members_url')

            if member_url:
                member_url = member_url[:member_url.index('{/member}')]
                member_urls.append((team['id'], member_url))

        if not len(member_urls):
            return None

        return member_urls

    def sink_and_broadcast(self):
        self.dest.sink(self.teams)

        member_urls = self.create_member_urls()

        if not member_urls:
            return

        evt = {
            'owner': self.owner,
            'data': []
        }

        for url in member_urls:
            evt['data'].append(url)

            if len(evt['data']) >= BATCH_SIZE:
                self.broadcaster.broadcast(evt)
                evt['data'] = []

        if len(evt['data']):
            self.broadcaster.broadcast(evt)

