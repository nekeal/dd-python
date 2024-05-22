from dataclasses import dataclass

from smartschedule.simulation.demand import Demand


@dataclass(frozen=True)
class Demands:
    all: tuple[Demand, ...]

    @classmethod
    def of(cls, *demands: Demand) -> "Demands":
        return Demands(demands)
