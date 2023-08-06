from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException

import json
import httpx

class CustomFieldExtractor(ExtractorBase):
    def __init__(
        self,
        owner: str,
        base_url: str,
        auth: Auth,
        dest: DataSink):
        super().__init__('jira', owner, 'custom_fields', base_url, auth, dest)

        self.url = f'{self.url_base}/rest/api/2/field'

    def extract(self):
        # print(f'To retrieve custom fields from {self.url}')
        
        auth = (self.auth.username, self.auth.password)
        resp = httpx.get(self.url, auth = auth)

        status = resp.status_code
        if status != httpx.codes.OK:
            msg = f'HTPP status {status} returned, not able to retrieve boards for {self.owner}. JIRA response: {resp.text}'
            raise UnknownHttpStatusException(status, msg)

        if (resp.text == '[]'):
            # print(f'WARNING! Empty response')
            return

        fields = json.loads(resp.text)
        
        # should never happen
        if not len(fields):
            return

        self.dest.sink(fields)



