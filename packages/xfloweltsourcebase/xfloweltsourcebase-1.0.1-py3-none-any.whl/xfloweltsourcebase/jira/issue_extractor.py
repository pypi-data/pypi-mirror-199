from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.jira.jira_events import IssueEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.base.exceptions import HttpStatus429Exception

from time import sleep
import json
import httpx

PAGE_SIZE = 50
BATCH_SIZE = 200

class IssueExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        featched_at: str,
        dest: DataSink, 
        broadcaster: IssueEventBroadcaster, 
        start_date: str,
        from_date: str,
        to_date: str,
        page_size = PAGE_SIZE):
        super().__init__('jira', owner, 'issues', base_url, auth, dest)

        self.broadcaster = broadcaster
        self.page_size = page_size
        self.featched_at = featched_at
        self.start_date = start_date
        self.from_date = from_date
        self.to_date = to_date

        self.url = f'{self.url_base}/rest/api/2/search'

    def extract(self):
        # print(f'To retrieve boards from {self.url}')
        
        start_at = 0

        params = {
            'maxResults': self.page_size,
            'jql': f'created>="{self.start_date}" AND updated>="{self.from_date}" AND updated<"{self.to_date}"'
        }

        auth = (self.auth.username, self.auth.password)
        issues = []
        iids = []

        while True:
            params['startAt'] = start_at

            # print(f'To retrieve issues at {self.url}, params: {params}')

            resp = httpx.get(self.url, auth = auth, params = params)
            status = resp.status_code

            if status == 429:
                # print(f'Too many request sent to JIRA for board issues. Owner: {self.owner}')
                raise HttpStatus429Exception()

            # 404 is not error
            if status == 404:
                break

            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve boards for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if (resp.text == '[]'):
                # print(f'WARNING! Empty response')
                break

            data = json.loads(resp.text)
            issues = [*issues, *data['issues']]

            if len(issues) >= BATCH_SIZE:
                self.sink_and_broadcast(issues)
                issues = []

            start_at += self.page_size

            if start_at >= data['total']:
                break

            # sleep 1 second so we don't hit JIRA too much
            sleep(1.0)

        if len(issues):
            self.sink_and_broadcast(issues)


    def sink_and_broadcast(self, issues):
        self.dest.sink(issues)

        iids = []
        for issue in issues:
            iids.append(issue['id'])

        evt = {
            'owner': self.owner,
            'issues': iids
        }

        self.broadcaster.broadcast(evt)
