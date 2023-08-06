from xfloweltsourcebase.base.events import BasicEventBroadcaster

class BoardEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('jira', owner, 'board_events')

class SprintEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('jira', owner, 'sprint_events')

class IssueEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('jira', owner, 'sprint_events')
