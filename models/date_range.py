from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DateRange:
    earliest: Optional[datetime] = None
    latest: Optional[datetime] = None