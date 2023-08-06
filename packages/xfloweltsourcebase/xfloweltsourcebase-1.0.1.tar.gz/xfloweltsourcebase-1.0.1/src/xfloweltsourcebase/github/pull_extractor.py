from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_events import PullReviewEventBroadcaster
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.base.utils import epoch, to_datetime
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx
from datetime import datetime

BATCH_SIZE = 10
PAGE_SIZE = 30
MAX_EXTRACTION_NUM = 150

# page -1 indicates the extraxtor needs to use end_date to calculate the fist page to be extracted

class PullExtractor(ExtractorBase):
    def __init__(
        self, 
        owner: str, 
        repo: str,
        base_url: str, 
        auth: Auth, 
        dest: DataSink, 
        broadcaster: PullReviewEventBroadcaster,
        end_date: datetime,
        last_updated: datetime = None,
        start_page = -1):
        super().__init__('github', owner, 'pulls', base_url, auth, dest)

        self.repo = repo
        self.broadcaster = broadcaster
        self.start_page = start_page
        self.end_date = end_date
        
        self.last_updated = last_updated
        if not self.last_updated:
            self.last_updated = epoch()

        self.extracted = 0
        self.next_page = start_page

        self.url = f'{self.url_base}/repos/{owner}/{repo}/pulls'
        self.pulls = []

    def extract(self):
        # print(f'To retrieve pulls from {self.url}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': PAGE_SIZE,
            'sort': 'updated',
            'direction': 'desc',
            'state': 'all'
        }

        page = self.start_page
        
        # we still have to start from page 1
        if page < 0:
            page = 1

        done = False
        last_updated = self.last_updated

        while not done:
            params['page'] = page

            resp = httpx.get(self.url, headers = headers, params = params)
            self.num_calls += 1

            status = resp.status_code

            if status == 422:
                # print(f'HTTP status 422(Unprocessable Entity) received. this is not an error')
                done = True
                continue

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
                done = True
                continue

            batch = json.loads(resp.text)

            for pull in batch:
                updated_at = to_datetime(pull['updated_at'])

                if updated_at < last_updated:
                    done = True
                    break

                if self.start_page < 0:
                    if updated_at > self.end_date:
                        continue

                self.pulls.append(pull)
                self.extracted += 1

            page += 1
            
            if self.extracted >= MAX_EXTRACTION_NUM:
                # print(f'Max number of retrieval reached. To try in next batch.')
                break

        if len(self.pulls):
            self.sink_and_broadcast()

        if self.extracted >= MAX_EXTRACTION_NUM:
            self.next_page = page
        else:
            self.next_page = -1

    def sink_and_broadcast(self):
        # print(f'# of pulls: {len(self.pulls)}')

        self.dest.sink(self.pulls)

        urls =[]
        reviews = []
        comments = []

        evt = {
            'owner': self.owner,
            'repo': self.repo,
            'reviews': [],
            'comments': [],
            'commits': [],
            'urls': []
        }

        for pull in self.pulls:
            evt['number'] = pull['number']
            evt['urls'].append(pull['url'])
            evt['reviews'].append(pull['url'] + '/reviews')
            evt['comments'].append(pull['url'] + '/comments')
            evt['commits'].append(pull['url'] + '/commits')

            if len(evt['urls']) >= BATCH_SIZE:
                self.broadcaster.broadcast(evt)

                evt['urls'] = []
                evt['reviews'] = []
                evt['comments'] = []
                evt['commits'] = []

        if len(evt['urls']):
            self.broadcaster.broadcast(evt)
