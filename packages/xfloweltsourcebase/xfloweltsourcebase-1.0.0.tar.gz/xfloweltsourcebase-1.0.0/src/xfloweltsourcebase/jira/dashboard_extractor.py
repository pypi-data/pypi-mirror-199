from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.jira.jira_events import BoardEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

from time import sleep
import json
import httpx

PAGE_SIZE = 50
BATCH_SIZE = 500

class DashboardExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        dest: DataSink, 
        start_date: str,
        page_size = PAGE_SIZE):
        super().__init__('jira', owner, 'dashboards', base_url, auth, dest)
        
        self.start_date = start_date
        self.page_size = page_size
        self.url = f'{self.url_base}/rest/api/2/dashboard'

    def extract(self):
        # print(f'To retrieve dashboards from {self.url}')

        start_at = 0

        params = {
            'maxResults': self.page_size,
            'jql': f'created>="{self.start_date}"'
        }

        auth = (self.auth.username, self.auth.password)


        boards = []

        while True:
            params['startAt'] = start_at

            resp = httpx.get(self.url, auth = auth, params = params)

            status = resp.status_code
            if status != httpx.codes.OK:
                raise UnknownHttpStatusException(status, f'HTPP status {status} returned, not able to retrieve boards for {self.owner}. JIRA response: {resp.text}')

            if (resp.text == '[]'):
                # print(f'WARNING! Empty response')
                break

            data = json.loads(resp.text)
            values = data.get('dashboards')

            if not values or not len(values):
                # print(f'WARNING! No data retrieved')
                break

            boards = [*boards, *values]

            if len(boards) >= BATCH_SIZE:
                self.dest.sink(boards)
                boards = []

            start_at += self.page_size

            if start_at >= data['total']:
                break

            # sleep 1 second so we don't hit JIRA too much
            sleep(1.0)

        if len(boards):
            self.dest.sink(boards)


