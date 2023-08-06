from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.constants import DFT_PAGE_SIZE
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.github.github_events import UserRepoBroadcaster

import json
import httpx

MEMBER_BATCH_SIZE = 1000

class MemberExtractor(ExtractorBase):
    def __init__(self, owner: str, base_url: str, auth: Auth, dest: DataSink, broadcaster: UserRepoBroadcaster, page_size = DFT_PAGE_SIZE):
        super().__init__('github', owner, 'members', base_url, auth, dest)

        self.url = self.url_base + '/orgs' + '/' + owner + '/members'
        self.page_size = page_size

        self.broadcaster = broadcaster

        self.members = []

    def extract(self):
        # print(f'To retrieve members for owner {self.owner}')

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

            self.members = [*self.members, *batched]

            if len(batched) < self.page_size:
                break


            page += 1

        if len(self.members):
            self.sink_and_broadcast()

    def sink_and_broadcast(self):
        # print(f'# of members: {len(self.members)}')

        self.dest.sink(self.members)

        evt = {
            'owner': self.owner,
            'members': self.members
        }

        self.broadcaster.broadcast(evt)
