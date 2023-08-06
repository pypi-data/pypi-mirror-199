from xfloweltsourcebase.base.exceptions import NotImplementedException

from typing import Union

class DataSink:
    def __init__(self, type: str, path: str):
        self.path = path

    def sink(self, data: Union[Union[str, dict], list]):
        raise NotImplementedException('sink not implemented')

