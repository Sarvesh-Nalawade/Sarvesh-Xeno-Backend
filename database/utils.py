import re
from datetime import datetime, timezone


def iso_to_utc(iso_ts: str) -> datetime:
    """Parse an ISO 8601 timestamp and return a naive UTC datetime

    Args:
        iso_ts (str): ISO-8601 timestamp string, e.g. "2025-09-11T12:13:18-04:00" or "2025-09-11T16:13:18Z"

    Returns:
        datetime: A naive datetime object in UTC timezone.

    Raises:
        ValueError: If the input string is not a valid ISO-8601 timestamp.

    Example:
        iso_to_utc_naive("2025-09-11T12:13:18-04:00")  -> datetime(2025,9,11,16,13,18)
    """

    if not iso_ts or not isinstance(iso_ts, str):
        raise ValueError("iso_ts must be a non-empty ISO-8601 string")

    s = iso_ts.strip()

    # normalize trailing Z -> +00:00 because datetime.fromisoformat doesn't accept 'Z'
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        # fallback: insert colon into timezone if format is like ...+HHMM or ...-HHMM
        m = re.match(r"^(.*)([+-]\d{2})(\d{2})$", s)
        if m:
            s = f"{m.group(1)}{m.group(2)}:{m.group(3)}"
            dt = datetime.fromisoformat(s)
        else:
            # can't parse
            raise

    # If timestamp is naive (no tz info), we assume it's already UTC.
    if dt.tzinfo is None:
        # return naive datetime (assumed UTC)
        return dt.replace(tzinfo=None)

    # Convert to UTC and return naive datetime
    dt_utc = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt_utc
