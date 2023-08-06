from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.constants import DFT_PAGE_SIZE
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

class TeamMemberExtractor(ExtractorBase):
    def __init__(self, auth: Auth, dest: DataSink, team_member_event: dict, page_size = DFT_PAGE_SIZE):
        super().__init__('github', '', 'team_members', '', auth, dest)
        self.event = team_member_event
        self.data = self.event.get('data')
        self.owner = self.event.get('owner')
        self.page_size = page_size

        self.members = []

    def extract(self):
        # print(f'To retrieve team members for owner {self.owner}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': self.page_size
        }

        for ele in self.data:
            team_id = ele[0]
            url = ele[1]

            page = 1

            while True:
                params['page'] = page

                resp = httpx.get(url, headers = headers, params = params)

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
                    raise UnknownHttpStatusException(status, f'Failed to retrieve team members at {url}')

                if resp.text == '[]':
                    # print(f'WARNING! empty response at {url}')
                    break

                ms = json.loads(resp.text)

                for member in ms:
                    member['team_id'] = team_id
                    self.members.append(member)

                if len(ms) < self.page_size:
                    break

                page += 1

        if len(self.members):
            self.dest.sink(self.members)
