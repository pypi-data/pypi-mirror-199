from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 1000
BATCH_SIZE = 3000

class UserExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        start_date: str):
        super().__init__('jira', owner, 'users', base_url, auth, dest)
        
        self.start_date = start_date

        # users/search?query for all users including inactive ones
        # user/search?query for only active users

        self.url = f'{self.url_base}/rest/api/2/users/search'

    def extract(self):
        start_at = 0

        # print(f'To retrieve users from {self.url}')
        
        # JIRA's group API doesn't offer paging, let's give it a big number and if the total
        # is greater than this value, we do another API call with the total number of groups
        params = {
            'maxResults': PAGE_SIZE,
            'query': '',
            'jql': f'created>="{self.start_date}"'
        }

        auth = (self.auth.username, self.auth.password)
        users = []

        while True:
            params['startAt'] = start_at

            resp = httpx.get(self.url, auth = auth, params = params)
            status = resp.status_code
        
            resp = httpx.get(self.url, auth = auth, params = params)
            status = resp.status_code

            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve users for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if resp.text == '[]':
                # print(f'WARNING! Empty response')
                break

            batched = json.loads(resp.text)
            num_records = len(batched)

            for user in batched:
                users.append(user)

            if len(users) >= BATCH_SIZE:
                self.dest.sink(users)
                users = []

            if num_records < PAGE_SIZE:
                break

            start_at += PAGE_SIZE

        if len(users):
            self.dest.sink(users)

        # print(f"Users for organization {self.owner} extracted. # of users: {len(users)}")