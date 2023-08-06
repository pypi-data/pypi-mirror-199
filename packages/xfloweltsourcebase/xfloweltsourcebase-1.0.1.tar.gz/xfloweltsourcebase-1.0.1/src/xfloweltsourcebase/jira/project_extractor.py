from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 50
BATCH_SIZE = 500

class ProjectExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        start_date: str):
        super().__init__('jira', owner, 'projects', base_url, auth, dest)
        
        self.start_date = start_date

        self.url = f'{self.url_base}/rest/api/2/project/search'

    def extract(self):
        # print(f'To retrieve projects from {self.url}')
        
        start_at = 0

        params = {
            'maxResults': PAGE_SIZE,
            'jql': f'created>="{self.start_date}"'
        }

        auth = (self.auth.username, self.auth.password)
        projects = []

        while True:
            params['startAt'] = start_at

            resp = httpx.get(self.url, auth = auth, params = params)
            status = resp.status_code

            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve projects for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if resp.text == '[]':
                # print(f'WARNING! Empty response')
                break

            data = json.loads(resp.text)
            values = data.get('values')

            for v in values:
                # print(f"To get project at {v['self']}")

                res = httpx.get(v['self'], auth = auth)
                sta = res.status_code

                if sta != httpx.codes.OK:
                    # print(f"ERROR! Failed to retrieve project from {v['self']}. status code: {sta}, server response: {res.text}")
                    continue

                if res.text == '[]':
                    continue

                projects.append(json.loads(res.text))

                if len(projects) >= BATCH_SIZE:
                    self.dest.sink(projects)
                    projects = []

            start_at += PAGE_SIZE

            if start_at >= data['total']:
                break

        if len(projects):
            self.dest.sink(projects)

        # print(f'Finished extracting projects for organization {self.owner}')