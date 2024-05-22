from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class TimeSlot:
    from_time: datetime
    to: datetime

    @staticmethod
    def create_daily_time_slot_at_utc(year: int, month: int, day: int) -> "TimeSlot":
        this_day = datetime(year, month, day)
        from_time = this_day
        return TimeSlot(from_time, from_time + timedelta(days=1))

    def within(self, other: "TimeSlot") -> bool:
        return self in other

    def __contains__(self, other: "TimeSlot") -> bool:
        return self.from_time <= other.from_time and self.to >= other.to
