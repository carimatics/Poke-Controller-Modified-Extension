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


def format_datetime(
    dt: datetime.datetime | None = None,
    fmt: str = "%Y-%m-%d_%H-%M-%S",
) -> str:
    if dt is None:
        return datetime.datetime.now().strftime(fmt)
    return dt.strftime(fmt)
