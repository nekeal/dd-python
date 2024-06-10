from dataclasses import dataclass, field

from smartschedule.allocation.allocated_capability import AllocatedCapability
from smartschedule.allocation.allocations import Allocations
from smartschedule.allocation.demands import Demands
from smartschedule.shared.time_slot import TimeSlot


@dataclass
class Project:
    demands: Demands
    earnings: float
    allocations: Allocations = field(default_factory=Allocations.none, init=False)

    def missing_demands(self) -> Demands:
        return self.demands.missing_demands(self.allocations)

    def remove(
        self, capability: AllocatedCapability, for_slot: TimeSlot
    ) -> AllocatedCapability | None:
        if (to_remove := self.allocations.find(capability, for_slot)) is None:
            return None
        self.allocations = self.allocations.remove(capability, for_slot)
        return to_remove

    def add(self, allocated_capability: AllocatedCapability) -> Allocations:
        self.allocations = self.allocations.add(allocated_capability)
        return self.allocations
