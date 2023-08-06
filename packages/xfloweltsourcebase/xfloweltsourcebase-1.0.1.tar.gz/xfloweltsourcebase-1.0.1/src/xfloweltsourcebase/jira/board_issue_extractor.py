from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.base.exceptions import HttpStatus429Exception

from time import sleep
import json
import httpx

PAGE_SIZE = 50
BATCH_SIZE = 500

class BoardIssueExtractor(ExtractorBase):
    def __init__(
        self,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        evt: dict,
        start_date: str,
        from_time: str,
        to_time: str,
        page_size = PAGE_SIZE):
        super().__init__('jira', '', 'board_issues', base_url, auth, dest)
        
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.board = evt['board']
        self.url_base = f'{self.url_base}/rest/agile/1.0/board/'
        self.page_size = page_size
        self.start_date = start_date
        self.from_time = from_time
        self.to_time = to_time

    def extract(self):
        # print(f'To extract board issuses. Organization: {self.owner}')
        
        auth = (self.auth.username, self.auth.password)

        jql = f'created>="{self.start_date}" and updated>="{self.from_time}" and updated<"{self.to_time}"'

        params =  {
            'maxResults': self.page_size,
            'jql': jql
        }

        url = f'{self.url_base}{str(self.board)}/issue'

        start_at = 0
        issues = []

        while True:
            params['startAt'] = start_at

            # print(f'To retrieve board issues at {url}, params: {params}')

            resp = httpx.get(url, auth = auth, params = params)
            status = resp.status_code

            if status == 429:
                # print(f'Too many request sent to JIRA for board issues. Owner: {self.owner}')
                raise HttpStatus429Exception()

            # 404 is not error
            if status == 404:
                break

            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve board issues for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if (resp.text == '[]'):
                # print(f'WARNING! Empty response')
                break

            data = json.loads(resp.text)
            # print(f"total issues: {data['total']}")

            for issue in data['issues']:
                issue['board'] = self.board
                issues.append(issue)

            if len(issues) >= BATCH_SIZE:
                self.dest.sink(issues)
                issues = []

            start_at += self.page_size

            if start_at >= data['total']:
                break

            # sleep 1 second so we don't hit JIRA too much
            sleep(1.0)

        if len(issues):
            self.dest.sink(issues)