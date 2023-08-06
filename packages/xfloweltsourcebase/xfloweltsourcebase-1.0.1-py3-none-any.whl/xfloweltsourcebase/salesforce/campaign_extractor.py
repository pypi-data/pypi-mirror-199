from xfloweltsourcebase.base.extractor_base import ExtractorBase
from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import UnknownHttpStatusException
from xfloweltsourcebase.salesforce.salesforce_exceptions import AuthorzationFailureException

import json
import httpx

from time import sleep

PAGE_SIZE = 50

class CampaignExtractor(ExtractorBase):
    def __init__(
        self, 
        owner: str, 
        domain_url: str, 
        api_version: str,
        auth: Auth, 
        dest: DataSink,
        created: str = None,
        updated_from: str = None,
        updated_end: str = None):
        super().__init__('salesforce', owner, 'campaigns', domain_url, auth, dest)
        self.api_version = api_version
        self.created = created
        self.updated_from = updated_from
        self.updated_end = updated_end

        self.campaigns = []

    def extract(self):
        url = f'{self.url_base}/services/data/{self.api_version}/query'
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth.token}'
        }

        query = self.__create_query_params()

        page = 0

        with httpx.Client(headers = headers) as client:
            while True:
                q = query
                
                if page:
                    q = f'{q} OFFSET {PAGE_SIZE * page}'

                # print(f'SOQL to be used: {q}')

                params = {
                    'q': q
                }

                resp = client.get(url, params = params)

                status = resp.status_code

                if status == 401:
                    self.auth.reauthorize()

                    if self.auth.authorized:
                        headers['Authorization'] = f'Bearer {self.auth.token}'
                        continue
                    else:
                        raise AuthorzationFailureException(self.auth.error)
                    
                if status == 429:
                    print(f'WARNING. Server responded with too many request. Sleep 10 seconds and try again')
                    sleep(10.0)
                    continue
                    
                if status != 200:
                    raise UnknownHttpStatusException(status, f'Salesforce response: {resp.text}')

                paged = json.loads(resp.text)

                size = paged['totalSize']

                if size:
                    for record in paged['records']:
                        record['account'] = self.owner
                        self.campaigns.append(record)

                if size < PAGE_SIZE:
                    break

                page += 1

        if len(self.campaigns):
            self.dest.sink(self.campaigns)

    def __create_query_params(self):
        if self.created:
            where = f'WHERE CreatedDate >= {self.created}'
        else:
            where = None

        if self.updated_from:
            if where:
                where = f'{where} AND LastModifiedDate >= {self.updated_from}'
            else:
                where = f'WHERE LastModifiedDate >= {self.updated_from}'

        if self.updated_end:
            if where:
                where = f'{where} AND LastModifiedDate < {self.updated_end}'
            else:
                where = f'WHERE LastModifiedDate < {self.updated_end}' 

        query = 'SELECT FIELDS(ALL) FROM Campaign'
        if where:
            query = f'{query} {where}'

        query = f'{query} LIMIT {PAGE_SIZE}'

        return query