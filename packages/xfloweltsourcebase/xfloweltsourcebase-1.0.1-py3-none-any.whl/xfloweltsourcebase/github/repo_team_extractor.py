from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.constants import DFT_PAGE_SIZE
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.github.github_exceptions import RateLimitReachedException

import json
import httpx

PAGE_SIZE = 100

class RepoTeamExtractor(ExtractorBase):
    def __init__(self, auth: Auth, dest: DataSink, team_member_event: dict):
        super().__init__('github', '', 'repo_teams', '', auth, dest)
        self.event = team_member_event
        self.data = self.event.get('data')
        self.owner = self.event.get('owner')

        self.repo_teams = []

    def extract(self):
        # print(f'To retrieve repo teams for owner {self.owner}')

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + self.auth.token
        }

        params = {
            'per_page': PAGE_SIZE
        }

        # print(f'data to be processed: {self.data}')

        for ele in self.data:
            repo_id = ele['repo']
            repo_name = ele['repoName']
            url = ele['teams']

            # print(f'To retrieve repo teams for owner {self.owner}, url: {url}')

            page = 1

            while True:
                params['page'] = page

                resp = httpx.get(url, headers = headers, params = params)

                status = resp.status_code

                # it is not an error, let's just break out. 422 = Unprocessable Entity
                if status == 422:
                    # print(f'HTTP status 422(Unprocessable Entity) received. this is not an error')
                    break

                if status == 404:
                    # print(f'HTTP status 404(Not Found) received. this is not an error. No teams retrieved for {url}')
                    break

                if status == 403:
                    remain = int(resp.headers.get('X-RateLimit-Remaining', 5000))
                    
                    if remain <= 0:
                        raise RateLimitReachedException(int(resp.headers.get('X-RateLimit-Reset')))
                    else:
                        raise UnknownHttpStatusException(status, f'Github response: {resp.text}')

                if status != 200:
                    # print(f"status {status} received for repo team {ele['repoName']}")
                    raise UnknownHttpStatusException(status, f'Failed to retrieve repo teams at {url}')

                if resp.text == '[]':
                    # if page == 1:
                    #     print(f"No teams found for repo {ele['repoName']}") 
                    # print(f'WARNING! empty response at {url}')
                    break

                teams = json.loads(resp.text)

                for team in teams:
                    self.repo_teams.append({
                        'repo_id': repo_id,
                        'repo_name': repo_name,
                        'slug': team['slug'],
                        'id': team['id'],
                        'name': team['name']
                    })

                if len(teams) < PAGE_SIZE:
                    break

                page += 1

        if len(self.repo_teams):
            # print(f'# of teams retrieved: {len(self.repo_teams)}')
            self.dest.sink(self.repo_teams)
