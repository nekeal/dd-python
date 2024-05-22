from dataclasses import dataclass, field

from smartschedule.simulation.demand import Demand
from smartschedule.simulation.demands import Demands
from smartschedule.simulation.project_id import ProjectId
from smartschedule.simulation.simulated_project import SimulatedProject


@dataclass
class SimulatedProjectsBuilder:
    current_id: ProjectId | None = None
    simulated_projects: list[ProjectId] = field(default_factory=list)
    simulated_demands: dict[ProjectId, Demands] = field(default_factory=dict)
    simulated_earnings: dict[ProjectId, float] = field(default_factory=dict)

    def with_project(self, id: ProjectId) -> "SimulatedProjectsBuilder":
        self.current_id = id
        self.simulated_projects.append(id)
        return self

    def that_requires(self, *demands: Demand) -> "SimulatedProjectsBuilder":
        assert self.current_id
        self.simulated_demands[self.current_id] = Demands.of(*demands)
        return self

    def that_can_earn(self, earnings: float) -> "SimulatedProjectsBuilder":
        assert self.current_id
        self.simulated_earnings[self.current_id] = earnings
        return self

    def build(self) -> list[SimulatedProject]:
        return [
            SimulatedProject(
                id, self.simulated_earnings[id], self.simulated_demands[id]
            )
            for id in self.simulated_projects
        ]
