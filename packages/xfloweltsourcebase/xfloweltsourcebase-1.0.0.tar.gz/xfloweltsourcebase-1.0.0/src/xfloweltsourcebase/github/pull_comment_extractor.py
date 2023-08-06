from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

PAGE_SIZE = 30

class PullCommentExtractor(ExtractorBase):
    def __init__(self, base_url: str, auth: Auth, dest: DataSink, evt: dict):
        super().__init__('github', '', 'pull_comments', base_url, auth, dest)

        self.owner = evt['owner']
        self.repo = evt['repo']
        self.urls = evt['comments']

        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        self.comments = []

        self.num_extracted = 0

    def __extract_and_sink(self, url):
        params = {
            'per_page': PAGE_SIZE
        }

        eindex = url.index('/comments')
        sindex = url.index('/pulls') + 7
        number = int(url[sindex:eindex])

        # print(f'to get comments at {url}, pull number: {number}')

        page = 1

        while True:
            params['page'] = page

            resp = httpx.get(url, headers = self.headers, params = params)
            self.num_calls += 1

            status = resp.status_code

            # foe below 2 status, they are not errors, let's just break out
            if status == 304 or status == 422:
                break

            if status == 403:
                remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))

                if remain <= 0:
                    raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
                else:
                    raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

            if status != 200:
                # print(f'WARNING: Got HTTP status {status} with GET at {url}')
                break

            self.num_success += 1

            if resp.text == '[]':
                # print(f'WARNING: Received empty response from GET at {url}')
                break

            coms = json.loads(resp.text)

            num = len(coms)

            self.num_extracted += num

            for comment in coms:
                comment['pull_number'] = number
                self.comments.append(comment)

            if num < PAGE_SIZE:
                break

            page += 1

    def extract(self):
        # print(f'To retrieve pull comments for repo {self.repo}')

        for url in self.urls:
            self.__extract_and_sink(url)

        if len(self.comments):
            self.dest.sink(self.comments)

        if self.num_extracted <= 0:
            # print(f'WARNING: No comments extracted for pulls {self.urls}')
            pass