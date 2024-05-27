from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class TimeSlot:
    from_: datetime
    to: datetime

    @classmethod
    def create_daily_time_slot_at_utc(
        cls, year: int, month: int, day: int
    ) -> "TimeSlot":
        this_day = datetime(year, month, day)
        from_ = this_day
        to = from_ + timedelta(days=1)
        return cls(from_, to)

    @classmethod
    def create_monthly_time_slot_at_utc(cls, year: int, month: int) -> "TimeSlot":
        start_of_month = datetime(year, month, 1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)
        from_ = start_of_month
        to = end_of_month
        return cls(from_, to)

    def within(self, other: "TimeSlot") -> bool:
        return self in other

    def __contains__(self, other: "TimeSlot") -> bool:
        return self.from_ <= other.from_ and self.to >= other.to
