from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

BATCH_SIZE = 500

class GroupExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        dest: DataSink,
        start_date: str):
        super().__init__('jira', owner, 'groups', base_url, auth, dest)
        
        self.start_date = start_date

        self.url = f'{self.url_base}/rest/api/2/groups/picker'
        self.member_url = f'{self.url_base}/rest/api/2/group/member'
        self.members = []

        self.auth = (auth.username, auth.password)

    def extract(self):
        # print(f'To retrieve groups from {self.url}')
        
        # JIRA's group API doesn't offer paging, let's give it a big number and if the total
        # is greater than this value, we do another API call with the total number of groups
        params = {
            'maxResults': 1000,
            'jql': f'created>="{self.start_date}"'
        }

        resp = httpx.get(self.url, auth = self.auth, params = params)
        status = resp.status_code

        if status != httpx.codes.OK:
            msg = f'HTTP status {status} returned, not able to retrieve groups for {self.owner}. JIRA response: {resp.text}'
            raise UnknownHttpStatusException(status, msg)

        if resp.text == '[]':
            # print(f'WARNING! Empty response')
            return

        data = json.loads(resp.text)

        if data['total'] > 1000:
            params = {
                'maxResults': data['total'],
                'jql': f'created>="{self.start_date}"'
            }

            resp = httpx.get(self.url, auth = self.auth, params = params)
            status = resp.status_code
            
            if status != httpx.codes.OK:
                msg = f'HTPP status {status} returned, not able to retrieve groups for {self.owner}. JIRA response: {resp.text}'
                raise UnknownHttpStatusException(status, msg)

            if resp.text == '[]':
                # print(f'WARNING! Empty response')
                return

            data = json.loads(resp.text)

        groups = data['groups']
        self.dest.sink(groups)

        self.extract_members(groups)

        # print(f"Groups for organization {self.owner} extracted. # of groups: {data['total']}")

    def extract_members(self, groups):
        if not groups or not len(groups):
            return

        for group in groups:
            group_id = group['groupId']
            group_name = group['name']
            params = {
                'maxResults': 50,
                'groupname': group_name,
                'includeInactiveUsers': True
            }

            start_at = 0

            # print(f'To extract members/users for group {group_name}')

            while True:
                params['startAt'] = start_at

                resp = httpx.get(self.member_url, auth = self.auth, params = params)

                status = resp.status_code
            
                if status != httpx.codes.OK:
                    # print(f'HTTP status {status} returned, not able to retrieve members/users for group {group_name}. JIRA response: {resp.text}')
                    break

                if resp.text == '[]':
                    # print(f'WARNING! Empty response')
                    break

                data = json.loads(resp.text)

                values = data.get('values')

                if not values or not len(values):
                    break

                for user in values:
                    user['groupId'] = group_id
                    user['groupName'] = group_name

                    self.members.append(user)

                total = int(data.get('total', 0))
                is_last = data.get('isLast', False)

                if is_last:
                    break

                start_at += 50

                if start_at >= total:
                    break