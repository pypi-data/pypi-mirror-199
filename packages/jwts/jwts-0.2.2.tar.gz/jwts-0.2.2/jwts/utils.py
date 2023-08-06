from calendar import timegm
from datetime import datetime


def to_unix_timestamp(timestamp: datetime) -> int:
    return timegm(timestamp.utctimetuple())
