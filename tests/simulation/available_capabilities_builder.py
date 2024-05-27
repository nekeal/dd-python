from dataclasses import dataclass, field
from uuid import UUID

from smartschedule.shared.time_slot import TimeSlot
from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)
from smartschedule.simulation.capability import Capability
from smartschedule.simulation.simulated_capabilities import SimulatedCapabilities


@dataclass
class AvailableCapabilitiesBuilder:
    availabilities: list[AvailableResourceCapability] = field(default_factory=list)
    current_resource_id: UUID | None = None
    capability: Capability | None = None
    time_slot: TimeSlot | None = None

    def with_employee(self, id_: UUID) -> "AvailableCapabilitiesBuilder":
        if self.current_resource_id is not None:
            assert self.capability and self.time_slot
            self.availabilities.append(
                AvailableResourceCapability(
                    self.current_resource_id, self.capability, self.time_slot
                )
            )
        self.current_resource_id = id_
        return self

    def that_brings(self, capability: Capability) -> "AvailableCapabilitiesBuilder":
        self.capability = capability
        return self

    def that_is_available_at(
        self, time_slot: TimeSlot
    ) -> "AvailableCapabilitiesBuilder":
        self.time_slot = time_slot
        return self

    def build(self) -> SimulatedCapabilities:
        if self.current_resource_id is not None:
            assert self.capability and self.time_slot
            self.availabilities.append(
                AvailableResourceCapability(
                    self.current_resource_id, self.capability, self.time_slot
                )
            )
        return SimulatedCapabilities(self.availabilities)
