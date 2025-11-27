import datetime


def from_timestamp(
    timestamp: float,
    timezone_delta: int | None = 9,
) -> datetime.datetime:
    tz = None
    if timezone_delta is not None:
        tz = datetime.timezone(datetime.timedelta(hours=timezone_delta))
    return datetime.datetime.fromtimestamp(
        timestamp=timestamp,
        tz=tz,
    )
