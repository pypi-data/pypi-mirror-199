from datetime import datetime, timezone

from xfloweltsourcebase.base.constants import GIT_TIMESTAMP_FORMAT
from xfloweltsourcebase.base.constants import JIRA_TIMESTAMP_FORMAT

# leave these 2 functions name as is for backward compatible
def to_datetime(tss) -> datetime:
    return datetime.strptime(tss, GIT_TIMESTAMP_FORMAT).replace(tzinfo = timezone.utc)

def to_datetime_str(ts) -> str:
    return ts.strftime(GIT_TIMESTAMP_FORMAT)

def epoch() -> datetime:
    return to_datetime('1970-01-01T00:00:00Z')

def to_jira_datetime(tss) -> datetime:
    return datetime.strptime(tss, JIRA_TIMESTAMP_FORMAT).replace(tzinfo = timezone.utc)

def to_jira_datetime_str(ts) -> str:
    return ts.strftime(JIRA_TIMESTAMP_FORMAT)
