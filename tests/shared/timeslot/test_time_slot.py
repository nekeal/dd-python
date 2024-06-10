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

    # as python tests
    def test_slots_overlapping(self):
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))
        slot2 = TimeSlot(datetime(2022, 1, 5), datetime(2022, 1, 15))
        slot3 = TimeSlot(datetime(2022, 1, 10), datetime(2022, 1, 20))
        slot4 = TimeSlot(datetime(2022, 1, 5), datetime(2022, 1, 10))
        slot5 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))

        assert slot1.overlaps_with(slot2)
        assert slot1.overlaps_with(slot1)
        assert slot1.overlaps_with(slot3)
        assert slot1.overlaps_with(slot4)
        assert slot1.overlaps_with(slot5)

    def test_slots_not_overlapping(self):
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))
        slot2 = TimeSlot(datetime(2022, 1, 10, 1), datetime(2022, 1, 20))
        slot3 = TimeSlot(datetime(2022, 1, 11), datetime(2022, 1, 20))

        assert not slot1.overlaps_with(slot2)
        assert not slot1.overlaps_with(slot3)

    def test_removing_common_parts_should_have_no_effect_when_there_is_no_overlap(self):
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))
        slot2 = TimeSlot(datetime(2022, 1, 15), datetime(2022, 1, 20))

        assert slot1.leftover_after_removing_common_with(slot2) == [slot1, slot2]

    def test_removing_common_parts_when_there_is_full_overlap(self):
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))

        assert slot1.leftover_after_removing_common_with(slot1) == []

    def test_removing_common_parts_when_there_is_overlap(self):
        # given
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 15))
        slot2 = TimeSlot(datetime(2022, 1, 10), datetime(2022, 1, 20))

        # when
        difference = slot1.leftover_after_removing_common_with(slot2)

        # then
        assert len(difference) == 2
        assert difference[0].from_ == datetime(2022, 1, 1)
        assert difference[0].to == datetime(2022, 1, 10)
        assert difference[1].from_ == datetime(2022, 1, 15)
        assert difference[1].to == datetime(2022, 1, 20)

        # given
        slot3 = TimeSlot(datetime(2022, 1, 5), datetime(2022, 1, 20))
        slot4 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 10))

        # when
        difference2 = slot3.leftover_after_removing_common_with(slot4)

        # then
        assert len(difference2) == 2
        assert difference2[0].from_ == datetime(2022, 1, 1)
        assert difference2[0].to == datetime(2022, 1, 5)
        assert difference2[1].from_ == datetime(2022, 1, 10)
        assert difference2[1].to == datetime(2022, 1, 20)

    def test_removing_common_part_when_one_slot_in_fully_within_another(self):
        # given
        slot1 = TimeSlot(datetime(2022, 1, 1), datetime(2022, 1, 20))
        slot2 = TimeSlot(datetime(2022, 1, 10), datetime(2022, 1, 15))

        # when
        difference = slot1.leftover_after_removing_common_with(slot2)

        # then
        assert len(difference) == 2
        assert difference[0].from_ == datetime(2022, 1, 1)
        assert difference[0].to == datetime(2022, 1, 10)
        assert difference[1].from_ == datetime(2022, 1, 15)
        assert difference[1].to == datetime(2022, 1, 20)
