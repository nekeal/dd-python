from dataclasses import dataclass, field

from smartschedule.allocation.allocated_capability import AllocatedCapability
from smartschedule.shared.time_slot import TimeSlot


@dataclass
class Allocations:
    all: set[AllocatedCapability] = field(default_factory=set)

    @staticmethod
    def none() -> "Allocations":
        return Allocations()

    def add(self, new_one: AllocatedCapability) -> "Allocations":
        self.all.add(new_one)
        return self

    def remove(self, to_remove: AllocatedCapability, slot: TimeSlot) -> "Allocations":
        found = self.find(to_remove, slot)
        if found is not None:
            self.all.remove(found)
            leftovers = found.time_slot.leftover_after_removing_common_with(slot)
            for leftover in leftovers:
                if leftover.within(found.time_slot):
                    self.all.add(
                        AllocatedCapability(
                            found.resource_id, found.capability, leftover
                        )
                    )
        return self

    def _remove_from_slot(
        self, allocated_resource: AllocatedCapability, slot: TimeSlot
    ) -> "Allocations":
        left_overs = [
            left_over
            for left_over in (
                allocated_resource.time_slot.leftover_after_removing_common_with(slot)
            )
            if left_over.within(allocated_resource.time_slot)
        ]
        new_slots = self.all - {allocated_resource}
        new_slots |= {
            AllocatedCapability(
                allocated_resource.resource_id, allocated_resource.capability, left_over
            )
            for left_over in left_overs
        }
        return Allocations(new_slots)

    def find(
        self, capability: AllocatedCapability, time_slot: TimeSlot
    ) -> AllocatedCapability | None:
        for ar in self.all:
            if ar == capability:
                return ar
        return None
