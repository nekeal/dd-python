from datetime import datetime

from smartschedule.shared.time_slot import TimeSlot


class TestTimeSlot:
    def test_creating_monthly_time_slot_at_utc(self):
        january2023 = TimeSlot.create_monthly_time_slot_at_utc(2023, 1)
        assert january2023.from_ == datetime(2023, 1, 1)
        assert january2023.to == datetime(2023, 2, 1)

    def test_creating_daily_time_slot_at_utc(self):
        specific_day = TimeSlot.create_daily_time_slot_at_utc(2023, 1, 15)
        assert specific_day.from_ == datetime(2023, 1, 15)
        assert specific_day.to == datetime(2023, 1, 16)

    def test_one_slot_within_another(self):
        slot1 = TimeSlot(datetime(2023, 1, 2), datetime(2023, 1, 2, 23, 59, 59))
        slot2 = TimeSlot(datetime(2023, 1, 1), datetime(2023, 1, 3))
        assert slot1.within(slot2)
        assert not slot2.within(slot1)

    def test_one_slot_is_not_within_another_if_they_just_overlap(self):
        slot1 = TimeSlot(datetime(2023, 1, 1), datetime(2023, 1, 1, 23, 59, 59))
        slot2 = TimeSlot(datetime(2023, 1, 2), datetime(2023, 1, 3))
        assert not slot1.within(slot2)
        assert not slot2.within(slot1)

        slot3 = TimeSlot(datetime(2023, 1, 2), datetime(2023, 1, 3, 23, 59, 59))
        slot4 = TimeSlot(datetime(2023, 1, 1), datetime(2023, 1, 2, 23, 59, 59))
        assert not slot3.within(slot4)
        assert not slot4.within(slot3)

    def test_slot_is_not_within_another_when_they_are_completely_outside(self):
        slot1 = TimeSlot(datetime(2023, 1, 1), datetime(2023, 1, 1, 23, 59, 59))
        slot2 = TimeSlot(datetime(2023, 1, 2), datetime(2023, 1, 3))
        assert not slot1.within(slot2)

    def test_slot_is_within_itself(self):
        slot1 = TimeSlot(datetime(2023, 1, 1), datetime(2023, 1, 1, 23, 59, 59))
        assert slot1.within(slot1)
