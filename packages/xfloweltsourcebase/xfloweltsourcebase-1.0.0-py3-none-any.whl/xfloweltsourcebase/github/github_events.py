from xfloweltsourcebase.base.events import BasicEventBroadcaster

class TeamMemberEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'team_member_events')

class CommitEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'commit_events')

class PullReviewEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'pull_review_events')

class IssueEventBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'issue_events')

class UserRepoBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'user_repos')

class RepoTeamBroadcaster(BasicEventBroadcaster):
    def __init__(self, owner: str):
        super().__init__('github', owner, 'repo_teams')

