from datetime import date, datetime
from typing import Any, Optional, Sequence

import click


class Date(click.DateTime):
    name = "date"

    def __init__(self, formats: Optional[Sequence[str]] = None):
        self.formats = formats or ["%Y-%m-%d"]

    def _try_to_convert_date(self, value: Any, format: str) -> Optional[date]:
        try:
            return datetime.strptime(value, format).date()
        except ValueError:
            return None

    def __repr__(self) -> str:
        return "Date"
