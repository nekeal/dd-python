from dataclasses import dataclass, field

from smartschedule.allocation.allocations import Allocations
from smartschedule.allocation.demand import Demand


@dataclass(frozen=True)
class Demands:
    all: list[Demand] = field(default_factory=list)

    def missing_demands(self, allocations: Allocations) -> "Demands":
        return Demands([d for d in self.all if not self._satisfied_by(d, allocations)])

    @staticmethod
    def _satisfied_by(d: Demand, allocations: Allocations) -> bool:
        return any(
            ar.capability == d.capability and d.slot.within(ar.time_slot)
            for ar in allocations.all
        )
