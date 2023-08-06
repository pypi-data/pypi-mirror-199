from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.jira.jira_events import BoardEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

from time import sleep
import json
import httpx


PAGE_SIZE = 50
BATCH_SIZE = 100

class BoardExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        featched_at: str,
        dest: DataSink, 
        broadcaster: BoardEventBroadcaster, 
        start_date: str,
        page_size = PAGE_SIZE):
        super().__init__('jira', owner, 'boards', base_url, auth, dest)
        
        self.broadcaster = broadcaster
        self.page_size = page_size
        self.featched_at = featched_at
        self.start_date = start_date

        self.url = f'{self.url_base}/rest/agile/1.0/board'

    def extract(self):
        # print(f'To retrieve boards from {self.url}')
        
        start_at = 0

        params = {
            'maxResults': self.page_size,
            'jql': f'created>="{self.start_date}"'
        }

        auth = (self.auth.username, self.auth.password)


        boards = []
        bids = []

        while True:
            params['startAt'] = start_at

            resp = httpx.get(self.url, auth = auth, params = params)

            status = resp.status_code
            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve boards for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if (resp.text == '[]'):
                # print(f'WARNING! Empty response')
                break

            data = json.loads(resp.text)
            values = data.get('values')

            if not values or not len(values):
                break

            for board in values:
                boards.append(board)
                bids.append(board['id'])

            if len(boards) >= BATCH_SIZE:
                self.sink_and_broadcast(boards, bids)

                boards = []
                bids = []

            total = data['total']

            if (start_at + self.page_size) >= total:
                break

            start_at += self.page_size

            # sleep 1 second so we don't hit JIRA too much
            sleep(1.0)

        if len(boards):
            self.sink_and_broadcast(boards, bids)

        # print(f'Finished extracting boards for organization {self.owner}')

    def sink_and_broadcast(self, boards, bids):
        # print(f'To save extracted boards to storage and broadcast events. Organization: {self.owner}, extract time: {self.featched_at}')

        self.dest.sink(boards)

        event = {
            'fetchedAt': self.featched_at,
            'owner': self.owner,
            'boards': bids
        }

        self.broadcaster.broadcast(event)




