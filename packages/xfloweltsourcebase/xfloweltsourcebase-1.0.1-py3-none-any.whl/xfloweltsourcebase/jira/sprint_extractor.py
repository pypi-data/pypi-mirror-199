from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.jira.jira_events import SprintEventBroadcaster

from time import sleep
import json
import httpx

PAGE_SIZE = 50
SAVE_BATCH_SIZE = 500
EVENT_BATCH_SIZE = 100

class SprintExtractor(ExtractorBase):
    def __init__(
        self,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        broadcaster: SprintEventBroadcaster,
        evt: dict,
        start_date: str):
        super().__init__('jira', '', 'sprints', base_url, auth, dest)
        
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.boards = evt['boards']
        self.url_base = f'{self.url_base}/rest/agile/1.0/'
        self.broadcaster = broadcaster
        self.start_date = start_date

    def extract(self):
        # print(f'To extract sprint issuses. Organization: {self.owner}')
        
        auth = (self.auth.username, self.auth.password)
        
        sprints = []

        # sprint issues
        event = {
            'fetchedAt': self.fetched_at,
            'owner': self.owner,
            'sprints': []
        }
        
        params =  {
            'maxResults': PAGE_SIZE,
            'jql': f'created>="{self.start_date}"'
        }

        for board in self.boards:
            url = f'{self.url_base}/board/{str(board)}/sprint'

            start_at = 0

            while True:
                params['startAt'] = start_at

                resp = httpx.get(url, auth = auth, params = params)
                status = resp.status_code

                if status != httpx.codes.OK:
                    # print(f'HTPP status {status} returned, not able to retrieve sprints for {self.owner}. JIRA response: {resp.text}')
                    break

                if (resp.text == '[]'):
                    # print(f'WARNING! Empty response')
                    break

                data = json.loads(resp.text)

                if not data.get('values') or not len(data.get('values')):
                    break

                for sprint in data['values']:
                    sprint['board'] = board
                    sprints.append(sprint)

                    event['sprints'].append(sprint['id'])

                if len(sprints) >= SAVE_BATCH_SIZE:
                    self.dest.sink(sprints)
                    sprints = []

                if len(event['sprints']) >= EVENT_BATCH_SIZE:
                    # print(f'sprint issues event to be broadcasted: {event}')
                    self.broadcaster.broadcast(event)
                    event['sprints'] = []

                if data['isLast']:
                    break

                start_at += PAGE_SIZE

        if len(sprints):
            self.dest.sink(sprints)

        if len(event['sprints']):
            # print(f'sprint issues event to be broadcasted: {event}')
            self.broadcaster.broadcast(event)

        
