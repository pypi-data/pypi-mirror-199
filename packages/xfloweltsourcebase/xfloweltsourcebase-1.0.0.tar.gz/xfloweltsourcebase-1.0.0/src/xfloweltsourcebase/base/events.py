from xfloweltsourcebase.base.exceptions import NotImplementedException

from typing import Union

class BasicEventBroadcaster:
    def __init__(self, database: str, owner: str, table: str):
        self.database = database
        self.owner = owner
        self.table = table

    def broadcast(self, data: Union[Union[str, dict], list]):
        raise NotImplementedException('broadcast_event not implemented')