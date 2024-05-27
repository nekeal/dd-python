from dataclasses import dataclass

from smartschedule.shared.supplier import Supplier
from smartschedule.simulation.demands import Demands
from smartschedule.simulation.project_id import ProjectId


@dataclass(frozen=True)
class SimulatedProject:
    project_id: ProjectId
    value: Supplier[float]
    missing_demands: Demands

    def calculate_value(self) -> float:
        return self.value.get()
