from datetime import datetime
from typing import Optional

import arrow
import dateparser


def parse_date_string(date: str) -> float:
    return dateparser.parse(date).timestamp()


def get_utc_date_ranges(
    from_time: datetime, to_time: Optional[datetime] = None, unit: str = "month"
):
    if to_time:
        end = arrow.get(to_time)
    else:
        end = arrow.utcnow()

    start = arrow.get(from_time).replace(hour=0, minute=0, second=0, microsecond=0)

    # print(f"from {start}")
    # print(f"to {end}")

    range = arrow.Arrow.span_range(unit, start=start, end=end, exact=True)  # type: ignore

    return [(s.datetime, e.datetime) for (s, e) in range]
