from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.base.utils import to_datetime
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

PAGE_SIZE = 100

class BranchExtractor(ExtractorBase):
    def __init__(
        self, 
        owner: str, 
        repo: str,
        base_url: str, 
        auth: Auth, 
        dest: DataSink):
        super().__init__('github', owner, 'branches', base_url, auth, dest)
        self.repo = repo

        self.url = f'{self.url_base}/repos/{owner}/{repo}/branches'

        self.branches = []

    def extract(self):
        # print(f'To retrieve branches from {self.url}')

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
            self.num_calls += 1

            status = resp.status_code

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

            self.num_success += 1

            if resp.text == '[]':
                break

            batched = json.loads(resp.text)

            for branch in batched:
                branch['repo'] = self.repo
                self.branches.append(branch)

            if len(batched) < PAGE_SIZE:
                break

            page += 1
            
        if len(self.branches):
            # print(f'# of branches for organization {self.owner} repository {self.repo}: {len(self.branches)}')
            self.dest.sink(self.branches)
        else:
            # print(f'WARNING: no branches found for organization {self.owner} repository {self.repo}')
            pass


