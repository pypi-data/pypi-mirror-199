from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 50
BATCH_SIZE = 500

class EpicExtractor(ExtractorBase):
    def __init__(
        self,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        evt: dict,
        start_date: str):
        super().__init__('jira', '', 'epics', base_url, auth, dest)
        
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.boards = evt['boards']
        self.url_base = f'{self.url_base}/rest/agile/1.0/board/'
        self.start_date = start_date

    def extract(self):
        # print(f'To extract board epics. Organization: {self.owner}')
        
        auth = (self.auth.username, self.auth.password)
        
        epics = []
        
        params =  {
            'maxResults': PAGE_SIZE,
            'jql': f'created>="{self.start_date}"'
        }

        for board in self.boards:
            url = f'{self.url_base}{str(board)}/epic'

            start_at = 0

            while True:
                params['startAt'] = start_at

                resp = httpx.get(url, auth = auth, params = params)
                status = resp.status_code

                if status != httpx.codes.OK:
                    raise UnknownHttpStatusException(status, f'HTPP status {status} returned, not able to retrieve epics for {self.owner}. JIRA response: {resp.text}')

                if (resp.text == '[]'):
                    # print(f'WARNING! Empty response')
                    break

                data = json.loads(resp.text)

                for value in data['values']:
                    value['board'] = board
                    epics.append(value)

                if len(epics) >= BATCH_SIZE:
                    self.dest.sink(epics)
                    epics = []

                if data['isLast']:
                        break

                start_at += PAGE_SIZE

        if len(epics):
            self.dest.sink(epics)