"""Date and time utility."""
from datetime import datetime

_SCHILLER_STD_DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_SCHILLER_STD_DATE_FORMAT = "%Y-%m-%d"


def datetime_to_str(d: datetime) -> str:
    """Converts a datetime object to a string as used in recordings."""
    time_str = datetime.strftime(d, _SCHILLER_STD_DT_FORMAT)
    return time_str


def str_to_datetime(s: str) -> datetime:
    """Converts a datetime string to a datetime object."""
    dt = datetime.strptime(s, _SCHILLER_STD_DT_FORMAT)
    return dt


def date_to_str(d: datetime) -> str:
    """Converts a `datetime.date` object to a string as used in recordings."""
    time_str = datetime.strftime(d, _SCHILLER_STD_DATE_FORMAT)
    return time_str


def str_to_date(s: str) -> datetime:
    """Converts a string to a `datetime.date` object."""
    dt = datetime.strptime(s, _SCHILLER_STD_DATE_FORMAT)
    return dt
