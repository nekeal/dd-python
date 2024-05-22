from dataclasses import dataclass

from smartschedule.simulation.demands import Demands
from smartschedule.simulation.project_id import ProjectId


@dataclass(frozen=True)
class SimulatedProject:
    project_id: ProjectId
    earnings: float
    missing_demands: Demands

    @property
    def all_demands_satisfied(self) -> bool:
        return not self.missing_demands
