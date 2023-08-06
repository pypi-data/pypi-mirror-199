from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import NotImplementedException

class ExtractorBase:
    def __init__(self, database: str, owner: str, table: str, url_base: str, auth: Auth, dest: DataSink):
        self.database = database
        self.owner = owner
        self.table = table
        self.dest = dest
        self.url_base = url_base.strip('/')
        self.auth = auth

        # statistics
        self.num_calls = 0
        self.num_success = 0

    def extract(self):
        raise NotImplementedException('extract not implemented')
