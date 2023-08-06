from xfloweltsourcebase.base.auth import Auth
from xfloweltsourcebase.base.data_sink import DataSink
from xfloweltsourcebase.base.exceptions import NotImplementedException

import logging

class ExtractorBase:
    def __init__(self, database: str, owner: str, table: str, url_base: str, auth: Auth, dest: DataSink, loggin_level = 'INFO'):
        self.database = database
        self.owner = owner
        self.table = table
        self.dest = dest
        self.url_base = url_base.strip('/')
        self.auth = auth

        # statistics
        self.num_calls = 0
        self.num_success = 0

        self.loggin_level = logging.getLevelName(loggin_level)

        self.logger = self.__create_logger()

    def extract(self):
        raise NotImplementedException('extract not implemented')

    def __create_logger(self):
        logger = logging.getLogger(self.__class__.__name__)

        handler = logging.FileHandler('/var/log/operator.log')
        handler.setLevel(self.logging_level)

        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(format)

        logger.addHandler(handler)

        return logger