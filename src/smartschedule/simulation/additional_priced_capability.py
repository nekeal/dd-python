from dataclasses import dataclass

from smartschedule.simulation.available_resource_capability import (
    AvailableResourceCapability,
)


@dataclass(frozen=True)
class AdditionalPricedCapability:
    value: float
    available_resource_capability: AvailableResourceCapability
