from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import HttpStatus429Exception

from time import sleep
import json
import httpx

PAGE_SIZE = 100
BATCH_SIZE = 1000

class IssueCommentExtractor(ExtractorBase):
    def __init__(
        self,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        evt: dict
    ):
        super().__init__('jira', '', 'issue_comments', base_url, auth, dest)
        
        self.owner = evt['owner']
        self.fetched_at = evt['fetchedAt']
        self.start_date = evt['startDate']
        self.issues = evt['issues']

        self.processed = []

    def extract(self):
        url_base = f'{self.url_base}/rest/api/2/issue/'
        # print(f'To retrieve boards from {url_base}')
        
        params =  {
            'maxResults': PAGE_SIZE,
            'jql': f'created>="{self.start_date}"'
        }

        auth = (self.auth.username, self.auth.password)
        comments = []

        for iid in self.issues:
            url = f'{url_base}{str(iid)}/comment'

            start_at = 0
            done = False

            while not done:
                params['startAt'] = start_at

                resp = httpx.get(url, auth = auth, params = params)
                status = resp.status_code

                if status == 429:
                    # print(f'Too many request sent to JIRA for issue comments. Owner: {self.owner}')
                    raise HttpStatus429Exception()

                if status != httpx.codes.OK:
                    # print(f'ERROR! Failed to extract comments from {url}. HTTP status: {status}, response: {resp.text}')
                    done = True
                else:
                    if resp.text == '[]':
                        done = True
                        continue

                    data = json.loads(resp.text)
                    comments = [*comments, *data['comments']]

                    start_at += PAGE_SIZE

                    if start_at >= data['total']:
                        done = True

                # sleep 1 second so we don't hit JIRA too much
                sleep(1.0)
                
            self.processed.append(iid)

            if len(comments) >= BATCH_SIZE:
                break

        if len(comments):
            self.dest.sink(comments)