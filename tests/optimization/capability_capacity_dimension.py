from dataclasses import dataclass, field
from uuid import UUID, uuid4

from smartschedule.optimization.capacity_dimension import CapacityDimension
from smartschedule.optimization.weight_dimension import WeightDimension
from smartschedule.shared.time_slot import TimeSlot


@dataclass(frozen=True)
class CapabilityCapacityDimension(CapacityDimension):
    uuid: UUID = field(default_factory=uuid4, init=False)
    id: str
    capacity_name: str
    capacity_type: str


@dataclass(frozen=True)
class CapabilityWeightDimension(WeightDimension[CapabilityCapacityDimension]):
    name: str
    type: str

    def is_satisfied_by(self, capacity_dimension: CapabilityCapacityDimension) -> bool:
        return (
            capacity_dimension.capacity_name == self.name
            and capacity_dimension.capacity_type == self.type
        )


@dataclass(frozen=True)
class CapabilityTimedCapacityDimension(CapacityDimension):
    uuid: UUID = field(default_factory=uuid4, init=False)
    id: str
    capacity_name: str
    capacity_type: str
    time_slot: TimeSlot


@dataclass(frozen=True)
class CapabilityTimedWeightDimension(WeightDimension[CapabilityTimedCapacityDimension]):
    name: str
    type: str
    time_slot: TimeSlot

    def is_satisfied_by(
        self, capacity_timed_dimension: CapabilityTimedCapacityDimension
    ) -> bool:
        return (
            capacity_timed_dimension.capacity_name == self.name
            and capacity_timed_dimension.capacity_type == self.type
            and self.time_slot.within(capacity_timed_dimension.time_slot)
        )
