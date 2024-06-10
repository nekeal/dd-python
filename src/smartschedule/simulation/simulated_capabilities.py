from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain

from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)


@dataclass
class SimulatedCapabilities:
    capabilities: list[AvailableResourceCapability]

    @classmethod
    def none(cls) -> "SimulatedCapabilities":
        return cls([])

    def add(
        self,
        new_capabilities: AvailableResourceCapability
        | Iterable[AvailableResourceCapability],
    ) -> "SimulatedCapabilities":
        if isinstance(new_capabilities, AvailableResourceCapability):
            return self._add_multiple([new_capabilities])
        return self._add_multiple(new_capabilities)

    def _add_multiple(
        self, new_capabilities: Iterable[AvailableResourceCapability]
    ) -> "SimulatedCapabilities":
        return SimulatedCapabilities(list(chain(self.capabilities, new_capabilities)))
